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
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository
from src.resource.logging.logger import logger


class RoleRepositoryImpl(RoleRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            logger.warn(f'[{RoleRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def createRole(self, role: Role):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN role
        '''

        bindVars = {"id": role.id(), "name": role.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        logger.debug(f'[{RoleRepositoryImpl.createRole.__qualname__}] Create role with id: {role.id()}, name: {role.name()}. Query result: {queryResult}')

    def roleByName(self, name: str) -> Role:
        aql = '''
            FOR u IN role
                FILTER u.name == @name
                RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RoleRepositoryImpl.roleByName.__qualname__}] {name}')
            raise RoleDoesNotExistException(name)

        return Role.createFrom(id=result[0]['id'], name=result[0]['name'])

    def roleById(self, id: str) -> Role:
        aql = '''
            FOR u IN role
                FILTER u.id == @id
                RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RoleRepositoryImpl.roleById.__qualname__}] role id: {id}')
            raise RoleDoesNotExistException(f'role id: {id}')

        return Role.createFrom(id=result[0]['id'], name=result[0]['name'])

    def deleteRole(self, role: Role) -> None:
        aql = '''
            FOR d IN role
                FILTER d.id == @id
                REMOVE d IN role
        '''

        bindVars = {"id": role.id()}
        logger.debug(f'[{RoleRepositoryImpl.deleteRole.__qualname__}] - Delete role with id: {role.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.roleById(role.id())
            logger.debug(
                f'[{RoleRepositoryImpl.deleteRole.__qualname__}] Object could not be found exception for role id: {role.id()}')
            raise ObjectCouldNotBeDeletedException(f'role id: {role.id()}')
        except RoleDoesNotExistException:
            role.publishDelete()

    def updateRole(self, role: Role) -> None:
        oldRole = self.roleById(role.id())
        if oldRole == role:
            logger.debug(
                f'[{RoleRepositoryImpl.updateRole.__qualname__}] Object identical exception for old role: {oldRole}\nrole: {role}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN role
                FILTER d.id == @id
                UPDATE d WITH {name: @name} IN role
        '''

        bindVars = {"id": role.id(), "name": role.name()}
        logger.debug(f'[{RoleRepositoryImpl.updateRole.__qualname__}] Update role with id: {role.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aRole = self.roleById(role.id())
        if aRole != role:
            logger.warn(
                f'[{RoleRepositoryImpl.updateRole.__qualname__}] The object role: {role} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'role: {role}')

    def rolesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN role #sortData RETURN d)
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
            return {"items": [Role.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}
