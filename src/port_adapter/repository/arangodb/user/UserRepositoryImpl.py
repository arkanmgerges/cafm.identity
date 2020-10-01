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
            raise Exception(f'[{UserRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

    def createUser(self, user: User):
        logger.debug(f'[{UserRepositoryImpl.createUser.__qualname__}] - with name = {user.name()}')
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name, password: @password}
            UPDATE {name: @name, password: @password }
          IN user
        '''

        bindVars = {"id": user.id(), "name": user.name(), "password": user.password()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def userByName(self, name: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByName.__qualname__}] - with name = {name}')
        aql = '''
            FOR u IN user
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(name)

        return User.createFrom(id=result[0]['id'], name=result[0]['name'], password=result[0]['password'])

    def userByNameAndPassword(self, name: str, password: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByNameAndPassword.__qualname__}] - with name = {name}')
        aql = '''
            FOR u IN user
            FILTER u.name == @name AND u.password == @password
            RETURN u
        '''

        bindVars = {"name": name, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(name)

        return User.createFrom(id=result[0]['id'], name=result[0]['name'], password=result[0]['password'])
