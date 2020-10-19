"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
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
        except Exception as e:
            raise Exception(
                f'[{PermissionRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

    def createPermission(self, permission: Permission):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN permission
        '''

        bindVars = {"id": permission.id(), "name": permission.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def permissionByName(self, name: str) -> Permission:
        aql = '''
            FOR u IN permission
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise PermissionDoesNotExistException(name)

        return Permission.createFrom(id=result[0]['id'], name=result[0]['name'])

    def permissionById(self, id: str) -> Permission:
        aql = '''
            FOR u IN permission
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise PermissionDoesNotExistException(f'permission id: {id}')

        return Permission.createFrom(id=result[0]['id'], name=result[0]['name'])

    def permissionsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                order: List[dict] = None) -> dict:
        sortData = ''
        if order is None:
            order = []
        else:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN permission #sortData RETURN d)
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
            return {"items": [Permission.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deletePermission(self, permission: Permission) -> None:
        aql = '''
            FOR d IN permission
            FILTER d.id == @id
            REMOVE d IN permission
        '''

        bindVars = {"id": permission.id()}
        logger.debug(
            f'[{PermissionRepositoryImpl.deletePermission.__qualname__}] - Delete permission with id: {permission.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is deleted
        try:
            self.permissionById(permission.id())
            raise ObjectCouldNotBeDeletedException()
        except PermissionDoesNotExistException:
            permission.publishDelete()

    def updatePermission(self, permission: Permission) -> None:
        oldPermission = self.permissionById(permission.id())
        if oldPermission == permission:
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN permission
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN permission
        '''

        bindVars = {"id": permission.id(), "name": permission.name()}
        logger.debug(
            f'[{PermissionRepositoryImpl.updatePermission.__qualname__}] - Update permission with id: {permission.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is updated
        aPermission = self.permissionById(permission.id())
        if aPermission != permission:
            raise ObjectCouldNotBeUpdatedException()
