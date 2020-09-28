"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domainmodel.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domainmodel.usergroup.UserGroup import UserGroup
from src.domainmodel.usergroup.UserGroupRepository import UserGroupRepository

from pyArango.connection import *


class UserGroupRepositoryImpl(UserGroupRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[UserGroupRepository::__init__] Could not connect to the db, message: {e}')

    def createUserGroup(self, userGroup: UserGroup):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN userGroup
        '''

        bindVars = {"id": userGroup.id(), "name": userGroup.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def userGroupByName(self, name: str) -> UserGroup:
        aql = '''
            FOR u IN userGroup
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserGroupDoesNotExistException(name)

        return UserGroup.createFrom(id=result[0]['id'], name=result[0]['name'])
