"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.connection import *
from pyArango.query import AQLQuery

from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.ResourceRepository import ResourceRepository
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class ResourceRepositoryImpl(ResourceRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            logger.warn(f'[{ResourceRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def resourceById(self, id: str = '') -> Resource:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{ResourceRepositoryImpl.resourceById.__qualname__}] resource id: {id}')
            raise RealmDoesNotExistException(f'resource id: {id}')

        return Resource(id=result[0]['id'], type=result[0]['type'])
