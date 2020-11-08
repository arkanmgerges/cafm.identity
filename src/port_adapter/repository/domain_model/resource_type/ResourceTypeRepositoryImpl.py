"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import PermissionContextDoesNotExistException
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
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
        except Exception as e:
            logger.warn(f'[{PermissionContextRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(
                f'Could not connect to the db, message: {e}')

    def createPermissionContext(self, permissionContext: PermissionContext):
        aql = '''
        UPSERT {id: @id, type: 'permission_context'}
            INSERT {id: @id, name: @name, type: 'permission_context'}
            UPDATE {name: @name}
          IN resource
        '''

        bindVars = {"id": permissionContext.id(), "name": permissionContext.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def permissionContextByName(self, name: str) -> PermissionContext:
        aql = '''
            FOR d IN resource
            FILTER d.name == @name AND d.type == 'permission_context'
            RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PermissionContextRepositoryImpl.permissionContextByName.__qualname__}] {name}')
            raise PermissionContextDoesNotExistException(name)

        return PermissionContext.createFrom(id=result[0]['id'], name=result[0]['name'])

    def permissionContextById(self, id: str) -> PermissionContext:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission_context'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PermissionContextRepositoryImpl.permissionContextById.__qualname__}] permissionContext id: {id}')
            raise PermissionContextDoesNotExistException(f'permission context id: {id}')

        return PermissionContext.createFrom(id=result[0]['id'], name=result[0]['name'])

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
            return {"items": [PermissionContext.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deletePermissionContext(self, permissionContext: PermissionContext) -> None:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission_context'
                REMOVE d IN resource
        '''

        bindVars = {"id": permissionContext.id()}
        logger.debug(
            f'[{PermissionContextRepositoryImpl.deletePermissionContext.__qualname__}] - Delete permissionContext with id: {permissionContext.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.permissionContextById(permissionContext.id())
            logger.debug(f'[{PermissionContextRepositoryImpl.deletePermissionContext.__qualname__}] Object could not be found exception for permission context id: {permissionContext.id()}')
            raise ObjectCouldNotBeDeletedException(f'permission context id: {permissionContext.id()}')
        except PermissionContextDoesNotExistException:
            permissionContext.publishDelete()

    def updatePermissionContext(self, permissionContext: PermissionContext) -> None:
        oldPermissionContext = self.permissionContextById(permissionContext.id())
        if oldPermissionContext == permissionContext:
            logger.debug(
                f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] Object identical exception for old permission context: {oldPermissionContext}\npermission context: {permissionContext}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission_context'
                UPDATE d WITH {name: @name} IN resource
        '''

        bindVars = {"id": permissionContext.id(), "name": permissionContext.name()}
        logger.debug(
            f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] - Update permissionContext with id: {permissionContext.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aPermissionContext = self.permissionContextById(permissionContext.id())
        if aPermissionContext != permissionContext:
            logger.warn(
                f'[{PermissionContextRepositoryImpl.updatePermissionContext.__qualname__}] The object permission context: {permissionContext} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'permission context: {permissionContext}')
