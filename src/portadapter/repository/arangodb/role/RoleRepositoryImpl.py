"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domainmodel.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domainmodel.role.Role import Role
from src.domainmodel.role.RoleRepository import RoleRepository

from pyArango.connection import *


class RoleRepositoryImpl(RoleRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[RoleRepository::__init__] Could not connect to the db, message: {e}')

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
