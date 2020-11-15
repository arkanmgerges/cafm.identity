"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission_context.PermissionContext import PermissionContext, PermissionContextConstant
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import \
    PermissionContextDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
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
        except Exception as e:
            logger.warn(
                f'[{PermissionContextRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(
                f'Could not connect to the db, message: {e}')

    def createPermissionContext(self, permissionContext: PermissionContext, tokenData: TokenData):
        actionFunction = '''
            function (params) {                                            
                let db = require('@arangodb').db;
                let res = db.permission_context.byExample({id: params['permission_context']['id'], type: params['permission_context']['type']}).toArray();
                if (res.length == 0) {
                    p = params['permission_context']
                    res = db.permission_context.insert({id: p['id'], name: p['name'], type: p['type']});
                    fromDocId = res['_id'];
                    p = params['permission_context']; p['fromId'] = fromDocId; p['fromType'] = params['permission_context']['type'];
                } else {
                    let err = new Error(`Could not create permission context, ${params['permission_context']['id']} is already exist`);
                    err.errorNum = params['OBJECT_ALREADY_EXIST_CODE'];
                    throw err;
                }
            }
        '''
        params = {
            'permission_context': {"id": permissionContext.id(), "data": permissionContext.data(),
                         "type": permissionContext.type()},
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['permission_context', 'owned_by']}, action=actionFunction, params=params)

    def updatePermissionContext(self, permissionContext: PermissionContext, tokenData: TokenData) -> None:
        oldObject = self.permissionContextById(permissionContext.id())
        if oldObject == permissionContext:
            logger.debug(
                f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] Object identical exception for old permission context: {oldObject}\npermission context: {permissionContext}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN permission_context
                FILTER d.id == @id
                UPDATE d WITH {data: @data, type: @type} IN permission_context
        '''

        bindVars = {"id": permissionContext.id(), "data": permissionContext.data(), "type": permissionContext.type()}
        logger.debug(
            f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] - Update permission context with id: {permissionContext.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        anObject = self.permissionContextById(permissionContext.id())
        if anObject != permissionContext:
            logger.warn(
                f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] The object permission context: {permissionContext} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'permission context: {permissionContext}')

    def deletePermissionContext(self, permissionContext: PermissionContext, tokenData: TokenData):
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
                'permission_context': {"id": permissionContext.id(), "data": permissionContext.data(),
                             "type": permissionContext.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['permission_context', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.permissionContextById(permissionContext.id())
            logger.debug(
                f'[{PermissionContextRepositoryImpl.deletePermissionContext.__qualname__}] Object could not be found exception for permission context id: {permissionContext.id()}')
            raise ObjectCouldNotBeDeletedException(f'permission context id: {permissionContext.id()}')

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

    def permissionContextsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                       order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN resource FILTER d.type == 'permission_context' #sortData RETURN d)
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
            return {"items": [PermissionContext.createFrom(id=x['id'], data=x['data']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}
