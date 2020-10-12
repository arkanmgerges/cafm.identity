"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository

from pyArango.connection import *


class OuRepositoryImpl(OuRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[{OuRepository.__init__.__qualname__}] Could not connect to the db, message: {e}')

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

    def ouById(self, id: str) -> Ou:
        aql = '''
            FOR u IN ou
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise OuDoesNotExistException(name=f'ou id: {id}')

        return Ou.createFrom(id=result[0]['id'], name=result[0]['name'])

    def ousByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Ou]:
        if 'super_admin' in ownedRoles:
            aql = '''
                FOR r IN ou
                Limit @resultFrom, @resultSize
                RETURN r
            '''
            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return []

            return [Ou.createFrom(id=x['id'], name=x['name']) for x in result]