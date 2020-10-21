"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.resource.logging.logger import logger


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
            logger.warn(f'[{OuRepository.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

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
            logger.debug(f'[{OuRepository.ouByName.__qualname__}] {name}')
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
            logger.debug(f'[{OuRepository.ouById.__qualname__}] ou id: {id}')
            raise OuDoesNotExistException(f'ou id: {id}')

        return Ou.createFrom(id=result[0]['id'], name=result[0]['name'])

    def ousByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                        order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN ou #sortData RETURN d)
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
            return {"items": [Ou.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deleteOu(self, ou: Ou) -> None:
        aql = '''
            FOR d IN ou
            FILTER d.id == @id
            REMOVE d IN ou
        '''

        bindVars = {"id": ou.id()}
        logger.debug(f'[{OuRepositoryImpl.deleteOu.__qualname__}] - Delete ou with id: {ou.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.ouById(ou.id())
            logger.debug(
                f'[{OuRepository.deleteOu.__qualname__}] Object could not be found exception for ou id: {ou.id()}')
            raise ObjectCouldNotBeDeletedException(f'ou id: {ou.id()}')
        except OuDoesNotExistException:
            ou.publishDelete()

    def updateOu(self, ou: Ou) -> None:
        oldOu = self.ouById(ou.id())
        if oldOu == ou:
            logger.debug(f'[{OuRepository.updateOu.__qualname__}] Object identical exception for old ou: {oldOu}\nou: {ou}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN ou
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN ou
        '''

        bindVars = {"id": ou.id(), "name": ou.name()}
        logger.debug(f'[{OuRepositoryImpl.updateOu.__qualname__}] - Update ou with id: {ou.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aOu = self.ouById(ou.id())
        if aOu != ou:
            logger.warn(f'[{OuRepositoryImpl.updateOu.__qualname__}] The object ou: {ou} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'ou: {ou}')
