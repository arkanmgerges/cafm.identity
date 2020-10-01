"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.AuthenticationRepository import AuthenticationRepository
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.resource.logging.logger import logger


class AuthenticationRepositoryImpl(AuthenticationRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[{AuthenticationRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

    def authenticateUserByNameAndPassword(self, name: str, password: str) -> dict:
        logger.debug(f'[{AuthenticationRepositoryImpl.authenticateUserByNameAndPassword.__qualname__}] - with name = {name}')
        aql = '''
                WITH role,userGroup
                FOR u IN user
                FILTER u.name == @name AND u.password == @password
                LET r1 = (FOR v,e IN 1..1 OUTBOUND u._id has FILTER e.toType == "role" RETURN v)
                LET r2 = (
                            FOR ug IN userGroup
                            FOR vUser,eUser IN 1..1 OUTBOUND ug._id has FILTER eUser.toType == "user" AND vUser._id == u._id
                            FOR vRole,eRole IN 1..1 OUTBOUND ug._id has FILTER eRole.toType == "role" RETURN vRole
                         )
                        RETURN {'id': u.id, 'name': u.name, 'role': union_distinct(r1, r2)[*].name}
              '''

        bindVars = {"name": name, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(name)

        result = result[0]
        return {'id': result['id'], 'name': result['name'], 'role': result['role']}


