"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository

from pyArango.connection import *


class OuRepositoryImpl(OuRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[OuRepository::__init__] Could not connect to the db, message: {e}')

    def createOu(self, ou: Ou):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN ou
        '''

        bindVars = {"id": ou.id(), "name": ou.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def ouByName(self, name: str) -> Ou:
        aql = '''
            FOR u IN ou
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise OuDoesNotExistException(name)

        return Ou.createFrom(id=result[0]['id'], name=result[0]['name'])
