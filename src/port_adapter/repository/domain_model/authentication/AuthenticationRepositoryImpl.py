"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os

import redis
from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.authentication.AuthenticationRepository import AuthenticationRepository
from src.domain_model.resource.exception.InvalidCredentialsException import InvalidCredentialsException
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class AuthenticationRepositoryImpl(AuthenticationRepository):
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
                f'[{AuthenticationRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

        try:
            self._cache = redis.Redis(host=os.getenv('CAFM_IDENTITY_REDIS_HOST', 'localhost'),
                                      port=os.getenv('CAFM_IDENTITY_REDIS_PORT', 6379))
            self._cacheSessionKeyPrefix = os.getenv('CAFM_IDENTITY_REDIS_SESSION_KEY_PREFIX',
                                                    'cafm.identity.session.')
        except Exception as e:
            raise Exception(
                f'[{AuthenticationRepositoryImpl.__init__.__qualname__}] Could not connect to the redis, message: {e}')

    @debugLogger
    def authenticateUserByEmailAndPassword(self, email: str, password: str) -> dict:
        logger.debug(
            f'[{AuthenticationRepositoryImpl.authenticateUserByEmailAndPassword.__qualname__}] - with name: {email}')
        aql = '''
                WITH resource
                FOR u IN resource
                FILTER u.email == @email AND u.password == @password AND u.type == 'user'
                LET r1 = (FOR v,e IN 1..1 OUTBOUND u._id has FILTER e._to_type == "role" RETURN v)
                LET r2 = (
                            FOR ug IN resource
                            FILTER ug.type == 'user_group'
                            LET r3 = (FOR vUser,eUser IN 1..1 OUTBOUND ug._id has FILTER eUser._to_type == "user" AND vUser._id == u._id RETURN ug._id)
                            FOR vRole,eRole IN 1..1 OUTBOUND r3[0].ug._id has FILTER eRole._to_type == "role" RETURN vRole
                         )
                LET r4 = union_distinct(r1, r2)
                LET r5 = (FOR d5 IN r4 RETURN {"id": d5.id, "name": d5.name})
                RETURN {'id': u.id, 'email': u.email, 'roles': r5}
              '''

        bindVars = {"email": email, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            res = self.authWithOneTimePassword(email=email, password=password)
            if res != {}:
                return res
            logger.info(
                f'[{AuthenticationRepositoryImpl.authenticateUserByEmailAndPassword.__qualname__}] - invalid credentials for user: {email}')
            raise InvalidCredentialsException(email)

        result = result[0]
        return {'id': result['id'], 'email': result['email'], 'roles': result['roles'], 'isOneTimePassword': False}

    def authWithOneTimePassword(self, email: str, password: str) -> dict:
        import src.port_adapter.AppDi as AppDi
        from src.domain_model.user.User import User
        from src.domain_model.authentication.AuthenticationService import AuthenticationService
        authService: AuthenticationService = AppDi.instance.get(AuthenticationService)
        logger.debug(
            f'[{AuthenticationRepositoryImpl.authWithOneTimePassword.__qualname__}] - with name: {email}')
        aql = '''
                WITH resource
                FOR u IN resource
                FILTER u.email == @email AND u.type == 'user'
                LET r1 = (FOR v,e IN 1..1 OUTBOUND u._id has FILTER e._to_type == "role" RETURN v)
                LET r2 = (
                            FOR ug IN resource
                            FILTER ug.type == 'user_group'
                            LET r3 = (FOR vUser,eUser IN 1..1 OUTBOUND ug._id has FILTER eUser._to_type == "user" AND vUser._id == u._id RETURN ug._id)
                            FOR vRole,eRole IN 1..1 OUTBOUND r3[0].ug._id has FILTER eRole._to_type == "role" RETURN vRole
                         )
                LET r4 = union_distinct(r1, r2)
                LET r5 = (FOR d5 IN r4 RETURN {"id": d5.id, "name": d5.name})
                RETURN {'id': u.id, 'email': u.email, 'password': u.password, 'roles': r5}
              '''

        bindVars = {"email": email}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        if len(result) == 0:
            return {}

        result = result[0]
        if 'password' in result and result['password'] is not None:
            dbPass: str = result['password']
            isOneTimePassword = User.ONE_TIME_PASSWORD_TAG in dbPass
            dbPass = dbPass.replace(User.ONE_TIME_PASSWORD_TAG, '')
            if authService.hashPassword(dbPass) == password:
                return {'id': result['id'], 'email': result['email'], 'roles': result['roles'],
                        'isOneTimePassword': isOneTimePassword}
        return {}

    @debugLogger
    def persistToken(self, token: str, ttl: int = 300) -> None:
        self._cache.setex(f'{self._cacheSessionKeyPrefix}{token}', ttl, token)

    @debugLogger
    def refreshToken(self, token: str, ttl: int = 300) -> None:
        self._cache.setex(f'{self._cacheSessionKeyPrefix}{token}', ttl, token)

    @debugLogger
    def tokenExists(self, token: str) -> bool:
        return self._cache.exists(f'{self._cacheSessionKeyPrefix}{token}') == 1

    @debugLogger
    def deleteToken(self, token: str) -> None:
        return self._cache.delete(f'{self._cacheSessionKeyPrefix}{token}')
