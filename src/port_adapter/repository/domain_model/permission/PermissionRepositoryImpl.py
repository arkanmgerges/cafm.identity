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

        except Exception as e:
            logger.warn(f'[{PermissionRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(
                f'Could not connect to the db, message: {e}')

    def createPermission(self, permission: Permission, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))

        actionFunction = '''
            function (params) {                                            
                queryLink = `UPSERT {_from: @fromId, _to: @toId}
                      INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                      UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                     IN owned_by`;

                let db = require('@arangodb').db;
                let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                if (res.length == 0) {
                    p = params['resource']
                    res = db.resource.insert({id: p['id'], name: p['name'], type: p['type']});
                    fromDocId = res['_id'];
                    p = params['user']; p['fromId'] = fromDocId; p['fromType'] = params['resource']['type'];
                    db._query(queryLink, p).execute();
                    for (let i = 0; i < params['permissionsDocIds'].length; i++) {
                        let currentDocId = params['permissionsDocIds'][i];
                        let p = {'fromId': fromDocId, 'toId': currentDocId, 
                            'fromType': params['resource']['type'], 'toType': params['toTypePermission']};
                        db._query(queryLink, p).execute();    
                    }
                } else {
                    let err = new Error(`Could not create resource, ${params['resource']['id']} is already exist`);
                    err.errorNum = params['OBJECT_ALREADY_EXIST_CODE'];
                    throw err;
                }
            }
        '''
        params = {
            'resource': {"id": permission.id(), "name": permission.name(), "type": permission.type()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)

    def updatePermission(self, permission: Permission, tokenData: TokenData) -> None:
        oldObject = self.permissionById(permission.id())
        if oldObject == permission:
            logger.debug(
                f'[{PermissionRepositoryImpl.updatePermission.__qualname__}] Object identical exception for old permission: {oldObject}\npermission: {permission}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission'
                UPDATE d WITH {name: @name} IN resource
        '''

        bindVars = {"id": permission.id(), "name": permission.name()}
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
                    let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                    if (res.length != 0) {
                        let doc = res[0];
                        let edges = db.owned_by.outEdges(doc._id);   
                        for (let i = 0; i < edges.length; i++) {
                            db.owned_by.remove(edges[i]);
                        }
                        db.resource.remove(doc);
                    } else {
                        let err = new Error(`Could not delete resource, ${params['resource']['id']}, it does not exist`);
                        err.errorNum = params['OBJECT_DOES_NOT_EXIST_CODE'];
                        throw err;
                    }
                }
            '''
            params = {
                'resource': {"id": permission.id(), "name": permission.name(), "type": permission.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.permissionById(permission.id())
            logger.debug(
                f'[{PermissionRepositoryImpl.deletePermission.__qualname__}] Object could not be found exception for permission id: {permission.id()}')
            raise ObjectCouldNotBeDeletedException(f'permission id: {permission.id()}')

    def permissionByName(self, name: str) -> Permission:
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'permission'
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
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission'
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

    def permissionsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN resource FILTER d.type == 'permission' #sortData RETURN d)
                RETURN {items: SLICE(ds, @resultFrom, @resultSize), itemCount: LENGTH(ds)}
            '''
            if sortData != '':
                aql = aql.replace('#sortData', f'SORT {sortData}')
            else:
                aql = aql.replace('#sortData', '')

            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return {"items": [], "itemCount": 0}
            return {
                "items": [Permission.createFrom(id=x['id'], name=x['name'], allowedActions=x['allowed_actions']) for x
                          in result[0]['items']],
                "itemCount": result[0]["itemCount"]}
