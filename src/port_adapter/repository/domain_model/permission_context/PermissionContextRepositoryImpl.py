"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.permission_context.PermissionContextRepository import (
    PermissionContextRepository,
)
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import (
    ObjectCouldNotBeDeletedException,
)
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import (
    ObjectCouldNotBeUpdatedException,
)
from src.domain_model.resource.exception.ObjectIdenticalException import (
    ObjectIdenticalException,
)
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import (
    PermissionContextDoesNotExistException,
)
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import (
    HelperRepository,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PermissionContextRepositoryImpl(PermissionContextRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
                username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
                password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
            )
            self._db = self._connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "")]
            self._helperRepo: HelperRepository = AppDi.instance.get(HelperRepository)
            self._policyService: PolicyControllerService = AppDi.instance.get(
                PolicyControllerService
            )
        except Exception as e:
            logger.warn(
                f"[{PermissionContextRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}"
            )
            raise Exception(f"Could not connect to the db, message: {e}")

    @debugLogger
    def bulkSave(self, objList: List[PermissionContext], tokenData: TokenData = None):
        self._upsertPermissionContexts(objList=objList, tokenData=tokenData)

    @debugLogger
    def bulkDelete(
            self, objList: List[PermissionContext], tokenData: TokenData = None
    ) -> None:
        self._deletePermissionContexts(objList=objList)

    @debugLogger
    def save(self, obj: PermissionContext, tokenData: TokenData = None):
        self._upsertPermissionContexts(objList=[obj], tokenData=tokenData)

    @debugLogger
    def _upsertPermissionContexts(self, objList: List[PermissionContext], tokenData: TokenData):
        actionFunction = """
            function (params) {                                            
                let db = require('@arangodb').db;
                let objList = params['permissionContextList'];
                for (let index in objList) {
                    res = db.permission_context.insert(
                        {
                            _key: objList[index].id,
                            id: objList[index].id,
                            type: objList[index].type,
                            data: objList[index].data
                        }, {"overwrite": true});
                }                
            }
        """
        params = {
            "permissionContextList": list(map(lambda obj: {
                "id": obj.id(),
                "type": obj.type(),
                "data": obj.data()
            }, objList))
        }
        self._db.transaction(
            collections={"write": ["permission_context"]},
            action=actionFunction,
            params=params,
        )

    @debugLogger
    def deletePermissionContext(self, obj: PermissionContext, tokenData: TokenData = None):
        try:
            self._deletePermissionContexts(objList=[obj])
        except Exception as e:
            print(e)
            self.permissionContextById(obj.id())
            logger.debug(
                f"[{PermissionContextRepositoryImpl.deletePermissionContext.__qualname__}] Object could not be found exception for permission context id: {obj.id()}"
            )
            raise ObjectCouldNotBeDeletedException(f"permission context id: {obj.id()}")

    def _deletePermissionContexts(self, objList: List[PermissionContext]):
        actionFunction = """
            function (params) {                                            
                let db = require('@arangodb').db;
                let idList = params['permissionContextIdList'];
                db.permission_context.removeByKeys(idList);
                for (let index in idList) {
                    db.for.removeByExample({_to: `permission_context/${idList[index]}`});
                }
            }
        """
        params = {
            "permissionContextIdList": list(map(lambda obj: obj.id(), objList))
        }
        self._db.transaction(
            collections={"write": ["permission_context", "for"]},
            action=actionFunction,
            params=params,
        )
    @debugLogger
    def permissionContextById(self, id: str) -> PermissionContext:
        aql = """
            FOR d IN permission_context
                FILTER d.id == @id
                RETURN d
        """

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PermissionContextRepositoryImpl.permissionContextById.__qualname__}] permission context id: {id}"
            )
            raise PermissionContextDoesNotExistException(f"permission context id: {id}")

        return PermissionContext.createFrom(
            id=result[0]["id"], type=result[0]["type"], data=result[0]["data"]
        )

    @debugLogger
    def permissionContexts(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        sortData = ""
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        result = self._policyService.permissionContextsByTokenData(
            tokenData, roleAccessPermissionData, sortData
        )

        if result is None or len(result["items"]) == 0:
            return {"items": [], "totalItemCount": 0}
        items = result["items"]
        totalItemCount = len(items)
        items = items[resultFrom : resultFrom + resultSize]

        return {
            "items": [
                PermissionContext.createFrom(id=x["id"], type=x["type"], data=x["data"])
                for x in items
            ],
            "totalItemCount": totalItemCount,
        }
