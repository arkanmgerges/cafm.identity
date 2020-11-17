"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.logger import logger


class PermissionRepositoryImpl(PermissionRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
            self._helperRepo: HelperRepository = AppDi.instance.get(HelperRepository)
            self._policyService: PolicyControllerService = AppDi.instance.get(PolicyControllerService)
        except Exception as e:
            logger.warn(f'[{PermissionRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(
                f'Could not connect to the db, message: {e}')

    def createPermission(self, permission: Permission, tokenData: TokenData):
        actionFunction = '''
            function (params) {                                            
                let db = require('@arangodb').db;
                let res = db.permission.byExample({id: params['permission']['id']}).toArray();
                if (res.length == 0) {
                    p = params['permission']
                    res = db.permission.insert({id: p['id'], name: p['name'], allowed_actions: p['allowed_actions'], denied_actions: p['denied_actions']});
                } else {
                    let err = new Error(`Could not create permission, ${params['permission']['id']} is already exist`);
                    err.errorNum = params['OBJECT_ALREADY_EXIST_CODE'];
                    throw err;
                }
            }
        '''
        params = {
            'permission': {"id": permission.id(), "name": permission.name(),
                           "allowed_actions": permission.allowedActions(),
                           "denied_actions": permission.deniedActions()},
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['permission', 'owned_by']}, action=actionFunction, params=params)

    def updatePermission(self, permission: Permission, tokenData: TokenData) -> None:
        oldObject = self.permissionById(permission.id())
        if oldObject == permission:
            logger.debug(
                f'[{PermissionRepositoryImpl.updatePermission.__qualname__}] Object identical exception for old permission: {oldObject}\npermission: {permission}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN permission
                FILTER d.id == @id
                UPDATE d WITH {name: @name, allowed_actions: @allowed_actions, denied_actions: @denied_actions} IN permission
        '''

        bindVars = {"id": permission.id(), "name": permission.name(), "allowed_actions": permission.allowedActions(),
                    "denied_actions": permission.deniedActions()}
        logger.debug(
            f'[{PermissionRepositoryImpl.updatePermission.__qualname__}] - Update permission with id: {permission.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        anObject = self.permissionById(permission.id())
        if anObject != permission:
            logger.warn(
                f'[{PermissionRepositoryImpl.updatePermission.__qualname__}] The object permission: {permission} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'permission: {permission}')

    def deletePermission(self, permission: Permission, tokenData: TokenData):
        try:
            actionFunction = '''
                function (params) {                                            
                    let db = require('@arangodb').db;
                    let res = db.permission.byExample({id: params['permission']['id']}).toArray();
                    if (res.length != 0) {
                        let doc = res[0];
                        db.permission.remove(doc);
                    } else {
                        let err = new Error(`Could not delete resource, ${params['permission']['id']}, it does not exist`);
                        err.errorNum = params['OBJECT_DOES_NOT_EXIST_CODE'];
                        throw err;
                    }
                }
            '''
            params = {
                'permission': {"id": permission.id(), "name": permission.name()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['permission', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.permissionById(permission.id())
            logger.debug(
                f'[{PermissionRepositoryImpl.deletePermission.__qualname__}] Object could not be found exception for permission id: {permission.id()}')
            raise ObjectCouldNotBeDeletedException(f'permission id: {permission.id()}')

    def permissionByName(self, name: str) -> Permission:
        aql = '''
            FOR d IN permission
                FILTER d.name == @name
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PermissionRepositoryImpl.permissionByName.__qualname__}] {name}')
            raise PermissionDoesNotExistException(name)

        return Permission.createFrom(id=result[0]['id'], name=result[0]['name'],
                                     allowedActions=result[0]['allowed_actions'])

    def permissionById(self, id: str) -> Permission:
        aql = '''
            FOR d IN permission
                FILTER d.id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PermissionRepositoryImpl.permissionById.__qualname__}] permission id: {id}')
            raise PermissionDoesNotExistException(
                f'permission id: {id}')

        return Permission.createFrom(id=result[0]['id'], name=result[0]['name'],
                                     allowedActions=result[0]['allowed_actions'])

    def permissions(self, tokenData: TokenData, roleAccessPermissionData:List[RoleAccessPermissionData], resultFrom: int = 0, resultSize: int = 100,
                        order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.permissionsByTokenData(tokenData, roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultSize]
        objectItems = []
        for x in items:
            allowedActions = x['allowed_actions'] if 'allowed_actions' in x else []
            deniedActions = x['denied_actions'] if 'denied_actions' in x else []
            objectItems.append(Permission.createFrom(id=x['id'], name=x['name'], allowedActions=allowedActions, deniedActions=deniedActions))
        return {"items": objectItems, "itemCount": itemCount}

