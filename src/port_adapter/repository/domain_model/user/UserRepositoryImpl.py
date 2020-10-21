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
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.resource.logging.logger import logger


class UserRepositoryImpl(UserRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            logger.warn(f'[{UserRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def createUser(self, user: User):
        logger.debug(f'[{UserRepositoryImpl.createUser.__qualname__}] - with name = {user.name()}')
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name, password: @password}
            UPDATE {name: @name, password: @password }
          IN user
        '''

        bindVars = {"id": user.id(), "name": user.name(), "password": user.password()}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

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
            logger.debug(f'[{UserRepositoryImpl.userByName.__qualname__}] {name}')
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
            logger.debug(f'[{UserRepositoryImpl.userByNameAndPassword.__qualname__}] name: {name}')
            raise UserDoesNotExistException(name)

        return User.createFrom(id=result[0]['id'], name=result[0]['name'], password=result[0]['password'])

    def userById(self, id: str) -> User:
        aql = '''
            FOR u IN user
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userById.__qualname__}] user id: {id}')
            raise UserDoesNotExistException(f'user id: {id}')

        return User.createFrom(id=result[0]['id'], name=result[0]['name'])

    def usersByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN user #sortData RETURN d)
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
            return {"items": [User.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deleteUser(self, user: User) -> None:
        aql = '''
            FOR d IN user
            FILTER d.id == @id
            REMOVE d IN user
        '''

        bindVars = {"id": user.id()}
        logger.debug(f'[{UserRepositoryImpl.deleteUser.__qualname__}] - Delete user with id: {user.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.userById(user.id())
            logger.debug(f'[{UserRepositoryImpl.deleteUser.__qualname__}] Object could not be deleted exception for user id: {user.id()}')
            raise ObjectCouldNotBeDeletedException(f'user id: {user.id()}')
        except UserDoesNotExistException:
            user.publishDelete()

    def updateUser(self, user: User) -> None:
        oldUser = self.userById(user.id())
        if oldUser == user:
            logger.debug(f'[{UserRepositoryImpl.updateUser.__qualname__}] Object identical exception for user id: {user.id()}')
            raise ObjectIdenticalException(f'user id: {user.id()}')

        aql = '''
            FOR d IN user
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN user
        '''

        bindVars = {"id": user.id(), "name": user.name()}
        logger.debug(f'[{UserRepositoryImpl.updateUser.__qualname__}] Update user with id: {user.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aUser = self.userById(user.id())
        if aUser != user:
            logger.warn(
                f'[{UserRepositoryImpl.updateUser.__qualname__}] The object user: {user} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException()
