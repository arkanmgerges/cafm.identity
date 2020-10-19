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
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository
from src.resource.logging.logger import logger


class ResourceTypeRepositoryImpl(ResourceTypeRepository):
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
                f'[{ResourceTypeRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

    def createResourceType(self, resourceType: ResourceType):
        aql = '''
        UPSERT { id: @id}
            INSERT {id: @id, name: @name}
            UPDATE {name: @name}
          IN resource_type
        '''

        bindVars = {"id": resourceType.id(), "name": resourceType.name()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        print(queryResult)

    def resourceTypeByName(self, name: str) -> ResourceType:
        aql = '''
            FOR u IN resource_type
            FILTER u.name == @name
            RETURN u
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise ResourceTypeDoesNotExistException(name)

        return ResourceType.createFrom(id=result[0]['id'], name=result[0]['name'])

    def resourceTypeById(self, id: str) -> ResourceType:
        aql = '''
            FOR u IN resource_type
            FILTER u.id == @id
            RETURN u
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise ResourceTypeDoesNotExistException(f'resourceType id: {id}')

        return ResourceType.createFrom(id=result[0]['id'], name=result[0]['name'])

    def resourceTypesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                  order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN resource_type #sortData RETURN d)
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
            return {"items": [ResourceType.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}

    def deleteResourceType(self, resourceType: ResourceType) -> None:
        aql = '''
            FOR d IN resource_type
            FILTER d.id == @id
            REMOVE d IN resource_type
        '''

        bindVars = {"id": resourceType.id()}
        logger.debug(
            f'[{ResourceTypeRepositoryImpl.deleteResourceType.__qualname__}] - Delete resourceType with id: {resourceType.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is deleted
        try:
            self.resourceTypeById(resourceType.id())
            raise ObjectCouldNotBeDeletedException()
        except ResourceTypeDoesNotExistException:
            resourceType.publishDelete()

    def updateResourceType(self, resourceType: ResourceType) -> None:
        oldResourceType = self.resourceTypeById(resourceType.id())
        if oldResourceType == resourceType:
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource_type
            FILTER d.id == @id
            UPDATE d WITH {name: @name} IN resource_type
        '''

        bindVars = {"id": resourceType.id(), "name": resourceType.name()}
        logger.debug(
            f'[{ResourceTypeRepositoryImpl.updateResourceType.__qualname__}] - Update resourceType with id: {resourceType.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        aResourceType = self.resourceTypeById(resourceType.id())
        if aResourceType != resourceType:
            raise ObjectCouldNotBeUpdatedException()
