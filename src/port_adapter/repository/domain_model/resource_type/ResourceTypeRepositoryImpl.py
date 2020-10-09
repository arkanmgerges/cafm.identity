"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.query import AQLQuery

from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository

from pyArango.connection import *


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
            raise Exception(f'[{ResourceTypeRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

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
            raise ResourceTypeDoesNotExistException(name=f'resourceType id: {id}')

        return ResourceType.createFrom(id=result[0]['id'], name=result[0]['name'])

    def resourceTypesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[ResourceType]:
        if 'super_admin' in ownedRoles:
            aql = '''
                FOR r IN resource_type
                Limit @resultFrom, @resultSize
                RETURN r
            '''
            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return []

            return [ResourceType.createFrom(id=x['id'], name=x['name']) for x in result]
