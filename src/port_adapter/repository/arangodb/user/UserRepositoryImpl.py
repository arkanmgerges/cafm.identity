"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository

from pyArango.connection import *

from src.resource.logging.logger import logger


class UserRepositoryImpl(UserRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[UserRepository::__init__] Could not connect to the db, message: {e}')

    def createUser(self, user: User):
        logger.debug(f'[{UserRepository.createUser.__qualname__}] - with name = {user.username()}')
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, username: @username, password: @password}
            UPDATE {username: @username, password: @password }
          IN user
        '''

        bindVars = {"id": user.id(), "username": user.username(), "password": user.password()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def userByUsername(self, username: str) -> User:
        logger.debug(f'[{UserRepository.userByUsername.__qualname__}] - with name = {username}')
        aql = '''
            FOR u IN user
            FILTER u.username == @username
            RETURN u
        '''

        bindVars = {"username": username}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(username)

        return User.createFrom(id=result[0]['id'], username=result[0]['username'], password=result[0]['password'])

    def userByUsernameAndPassword(self, username: str, password: str) -> User:
        logger.debug(f'[{UserRepository.userByUsernameAndPassword.__qualname__}] - with name = {username}')
        aql = '''
            FOR u IN user
            FILTER u.username == @username AND u.password == @password
            RETURN u
        '''

        bindVars = {"username": username, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(username)

        return User.createFrom(id=result[0]['id'], username=result[0]['username'], password=result[0]['password'])
