"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import \
    PermissionContextDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PermissionContextRepositoryImpl(PermissionContextRepository):
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
            logger.warn(
                f'[{PermissionContextRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(
                f'Could not connect to the db, message: {e}')

    @debugLogger
    def save(self, obj: PermissionContext, tokenData: TokenData = None):
        try:
            user = self.permissionContextById(id=obj.id())
            if user != obj:
                self.updatePermissionContext(obj=obj, tokenData=tokenData)
        except PermissionContextDoesNotExistException as _e:
            self.createPermissionContext(obj=obj, tokenData=tokenData)

    @debugLogger
    def createPermissionContext(self, obj: PermissionContext, tokenData: TokenData):
        actionFunction = '''
            function (params) {                                            
                let db = require('@arangodb').db;
                let res = db.permission_context.byExample({id: params['permission_context']['id'], type: params['permission_context']['type']}).toArray();
                if (res.length == 0) {
                    p = params['permission_context']
                    res = db.permission_context.insert({id: p['id'], data: p['data'], type: p['type']});
                } else {
                    let err = new Error(`Could not create permission context, ${params['permission_context']['id']} is already exist`);
                    err.errorNum = params['OBJECT_ALREADY_EXIST_CODE'];
                    throw err;
                }
            }
        '''
        params = {
            'permission_context': {"id": obj.id(), "data": obj.data(),
                                   "type": obj.type()},
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['permission_context']}, action=actionFunction, params=params)

    @debugLogger
    def updatePermissionContext(self, obj: PermissionContext, tokenData: TokenData) -> None:
        repoObj = self.permissionContextById(obj.id())
        if repoObj != obj:
            aql = '''
                FOR d IN permission_context
                    FILTER d.id == @id
                    UPDATE d WITH {data: @data, type: @type} IN permission_context
            '''

            bindVars = {"id": obj.id(), "data": obj.data(), "type": obj.type()}
            logger.debug(
                f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] - Update permission context with id: {obj.id()}')
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

            # Check if it is updated
            repoObj = self.permissionContextById(obj.id())
            if repoObj != obj:
                logger.warn(
                    f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] The object permission context: {obj} could not be updated in the database')
                raise ObjectCouldNotBeUpdatedException(f'permission context: {obj}')

    @debugLogger
    def deletePermissionContext(self, obj: PermissionContext, tokenData: TokenData = None):
        try:
            actionFunction = '''
                function (params) {                                            
                    let db = require('@arangodb').db;
                    let res = db.permission_context.byExample({id: params['permission_context']['id'], type: params['permission_context']['type'], data: params['permission_context']['data']}).toArray();
                    if (res.length != 0) {
                        let doc = res[0];
                        db.permission_context.remove(doc);
                    } else {
                        let err = new Error(`Could not delete permission context, ${params['permission_context']['id']}, it does not exist`);
                        err.errorNum = params['OBJECT_DOES_NOT_EXIST_CODE'];
                        throw err;
                    }
                }
            '''
            params = {
                'permission_context': {"id": obj.id(), "data": obj.data(),
                                       "type": obj.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['permission_context', 'owned_by']}, action=actionFunction,
                                 params=params)
        except Exception as e:
            print(e)
            self.permissionContextById(obj.id())
            logger.debug(
                f'[{PermissionContextRepositoryImpl.deletePermissionContext.__qualname__}] Object could not be found exception for permission context id: {obj.id()}')
            raise ObjectCouldNotBeDeletedException(f'permission context id: {obj.id()}')

    @debugLogger
    def permissionContextById(self, id: str) -> PermissionContext:
        aql = '''
            FOR d IN permission_context
                FILTER d.id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f'[{PermissionContextRepositoryImpl.permissionContextById.__qualname__}] permission context id: {id}')
            raise PermissionContextDoesNotExistException(f'permission context id: {id}')

        return PermissionContext.createFrom(id=result[0]['id'], type=result[0]['type'], data=result[0]['data'])

    @debugLogger
    def permissionContexts(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData],
                           resultFrom: int = 0, resultSize: int = 100,
                           order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        result = self._policyService.permissionContextsByTokenData(tokenData, roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]

        return {"items": [PermissionContext.createFrom(id=x['id'], type=x['type'], data=x['data']) for x in items],
                "itemCount": itemCount}
