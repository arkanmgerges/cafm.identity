"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.resource.logging.logger import logger


class RealmRepositoryImpl(RealmRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            logger.warn(f'[{RealmRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def createRealm(self, realm: Realm):
        aql = '''
        UPSERT {id: @id}
            INSERT {id: @id, name: @name, _type: 'realm'}
            UPDATE {name: @name}
          IN resource
        '''

        bindVars = {"id": realm.id(), "name": realm.name()}
        logger.debug(f'[{RealmRepositoryImpl.createRealm.__qualname__}] Upsert for id: {realm.id()}, name: {realm.name()}')
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def realmByName(self, name: str) -> Realm:
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'realm'
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RealmRepositoryImpl.realmByName.__qualname__}] {name}')
            raise RealmDoesNotExistException(name)

        return Realm.createFrom(id=result[0]['id'], name=result[0]['name'])

    def realmById(self, id: str) -> Realm:
        aql = '''
            FOR d IN realm
                FILTER d.id == @id AND d.type == 'realm'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RealmRepositoryImpl.realmById.__qualname__}] realm id: {id}')
            raise RealmDoesNotExistException(f'realm id: {id}')

        return Realm.createFrom(id=result[0]['id'], name=result[0]['name'])

    def realmsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                           order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN resource FILTER d.type == 'realm' #sortData RETURN d)
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
            return {"items": [Realm.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deleteRealm(self, realm: Realm) -> None:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'realm'
                REMOVE d IN resource
        '''

        bindVars = {"id": realm.id()}
        logger.debug(f'[{RealmRepositoryImpl.deleteRealm.__qualname__}] - Delete realm with id: {realm.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.realmById(realm.id())
            logger.debug(f'[{RealmRepositoryImpl.deleteRealm.__qualname__}] Object could not be found exception for realm id: {realm.id()}')
            raise ObjectCouldNotBeDeletedException(f'realm id: {realm.id()}')
        except RealmDoesNotExistException:
            realm.publishDelete()

    def updateRealm(self, realm: Realm) -> None:
        oldRealm = self.realmById(realm.id())
        if oldRealm == realm:
            logger.debug(f'[{RealmRepositoryImpl.updateRealm.__qualname__}] Object identical exception for old realm: {oldRealm}\nrealm: {realm}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'realm'
                UPDATE d WITH {name: @name} IN resource
        '''

        bindVars = {"id": realm.id(), "name": realm.name()}
        logger.debug(f'[{RealmRepositoryImpl.updateRealm.__qualname__}] - Update realm with id: {realm.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aRealm = self.realmById(realm.id())
        if aRealm != realm:
            logger.warn(f'[{RealmRepositoryImpl.updateRealm.__qualname__}] The object realm: {realm} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'realm: {realm}')
