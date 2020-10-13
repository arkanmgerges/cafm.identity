"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository

from pyArango.connection import *

from src.resource.logging.logger import logger


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

    def deleteUserGroup(self, userGroup: UserGroup) -> None:
        aql = '''
            FOR d IN user_group
            FILTER d.id == @id
            REMOVE d IN user_group
        '''

        bindVars = {"id": userGroup.id()}
        logger.debug(f'[{UserGroupRepositoryImpl.deleteUserGroup.__qualname__}] - Delete userGroup with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is deleted
        try:
            self.userGroupById(userGroup.id())
            raise ObjectCouldNotBeDeletedException()
        except UserGroupDoesNotExistException:
            userGroup.publishDelete()

    def updateUserGroup(self, userGroup: UserGroup) -> None:
        oldUserGroup = self.userGroupById(userGroup.id())
        if oldUserGroup == userGroup:
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN user_group
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN user_group
        '''

        bindVars = {"id": userGroup.id(), "name": userGroup.name()}
        logger.debug(f'[{UserGroupRepositoryImpl.updateUserGroup.__qualname__}] - Update userGroup with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        # Check if it is updated
        aUserGroup = self.userGroupById(userGroup.id())
        if aUserGroup != userGroup:
            raise ObjectCouldNotBeUpdatedException()