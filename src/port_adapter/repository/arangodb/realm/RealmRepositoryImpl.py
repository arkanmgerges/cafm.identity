"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository

from pyArango.connection import *


class RealmRepositoryImpl(RealmRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CORAL_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CORAL_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CORAL_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CORAL_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            raise Exception(f'[RealmRepository::__init__] Could not connect to the db, message: {e}')

    def createRealm(self, realm: Realm):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN realm
        '''

        bindVars = {"id": realm.id(), "name": realm.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def realmByName(self, name: str) -> Realm:
        aql = '''
            FOR u IN realm
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise RealmDoesNotExistException(name)

        return Realm.createFrom(id=result[0]['id'], name=result[0]['name'])
