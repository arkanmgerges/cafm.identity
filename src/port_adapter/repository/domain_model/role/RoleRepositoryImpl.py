"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository

from pyArango.connection import *


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
            raise Exception(f'[{RoleRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

    def createRole(self, role: Role):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN role
        '''

        bindVars = {"id": role.id(), "name": role.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

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
            raise RoleDoesNotExistException(name=f'role id: {id}')

        return Role.createFrom(id=result[0]['id'], name=result[0]['name'])

    def rolesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Role]:
        if 'super_admin' in ownedRoles:
            aql = '''
                FOR r IN role
                Limit @resultFrom, @resultSize
                RETURN r
            '''
            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return []

            return [Role.createFrom(id=x['id'], name=x['name']) for x in result]
