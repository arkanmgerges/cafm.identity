"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository

from pyArango.connection import *


class UserGroupRepositoryImpl(UserGroupRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[UserGroupRepository::__init__] Could not connect to the db, message: {e}')

    def createUserGroup(self, userGroup: UserGroup):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN user_group
        '''

        bindVars = {"id": userGroup.id(), "name": userGroup.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def userGroupByName(self, name: str) -> UserGroup:
        aql = '''
            FOR u IN user_group
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserGroupDoesNotExistException(name)

        return UserGroup.createFrom(id=result[0]['id'], name=result[0]['name'])

    def userGroupById(self, id: str) -> UserGroup:
        aql = '''
            FOR u IN user_group
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserGroupDoesNotExistException(name=f'userGroup id: {id}')

        return UserGroup.createFrom(id=result[0]['id'], name=result[0]['name'])

    def userGroupsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[UserGroup]:
        if 'super_admin' in ownedRoles:
            aql = '''
                FOR r IN user_group
                Limit @resultFrom, @resultSize
                RETURN r
            '''
            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return []

            return [UserGroup.createFrom(id=x['id'], name=x['name']) for x in result]
