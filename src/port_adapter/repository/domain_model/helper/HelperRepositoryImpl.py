"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.RoleDoesNotExistException import (
    RoleDoesNotExistException,
)
from src.domain_model.resource.exception.UserDoesNotExistException import (
    UserDoesNotExistException,
)
from src.port_adapter.repository.domain_model.helper.HelperRepository import (
    HelperRepository,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class HelperRepositoryImpl(HelperRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
                username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
                password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
            )
            self._db = self._connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "")]
        except Exception as e:
            logger.warn(
                f"[{HelperRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}"
            )
            raise Exception(f"Could not connect to the db, message: {e}")

    @debugLogger
    def roleDocumentId(self, id: str):
        # Get the role doc id
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'role'
                RETURN d
        """
        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{HelperRepositoryImpl.roleDocumentId.__qualname__}] role id: {id}"
            )
            raise RoleDoesNotExistException(f"role id: {id}")
        result = result[0]
        roleDocId = result["_id"]
        return roleDocId

    @debugLogger
    def userDocumentId(self, id: str):
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                RETURN d
        """
        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{HelperRepositoryImpl.userDocumentId.__qualname__}] user id: {id}"
            )
            raise UserDoesNotExistException(f"user id: {id}")
        result = result[0]
        userDocId = result["_id"]
        return userDocId

    @debugLogger
    def resourceDocumentId(self, resource: Resource):
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == @type
                RETURN d
        """
        bindVars = {"id": resource.id(), "type": resource.type()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{HelperRepositoryImpl.resourceDocumentId.__qualname__}] resource id: {resource.id()}"
            )
            raise RoleDoesNotExistException(f"resource id: {resource.id()}")
        result = result[0]
        docId = result["_id"]
        return docId
