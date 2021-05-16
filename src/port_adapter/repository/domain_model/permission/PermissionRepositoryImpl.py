"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
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
from src.domain_model.resource.exception.PermissionDoesNotExistException import (
    PermissionDoesNotExistException,
)
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import (
    HelperRepository,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PermissionRepositoryImpl(PermissionRepository):
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
                f"[{PermissionRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}"
            )
            raise Exception(f"Could not connect to the db, message: {e}")

    @debugLogger
    def bulkSave(self, objList: List[Permission], tokenData: TokenData = None):
        self._upsertPermissions(objList=objList, tokenData=tokenData)

    @debugLogger
    def bulkDelete(
            self, objList: List[Permission], tokenData: TokenData = None
    ) -> None:
        self._deletePermissions(objList=objList)

    @debugLogger
    def save(self, obj: Permission, tokenData: TokenData = None):
        self._upsertPermissions(objList=[obj], tokenData=tokenData)

    @debugLogger
    def _upsertPermissions(self, objList: List[Permission], tokenData: TokenData):
        actionFunction = """
            function (params) {                                            
                let db = require('@arangodb').db;
                let objList = params['permissionList'];
                for (let index in objList) {
                    res = db.permission.insert(
                        {
                            _key: objList[index].id,
                            id: objList[index].id,
                            name: objList[index].name,
                            allowed_actions: objList[index].allowed_actions,
                            denied_actions: objList[index].denied_actions
                        }, {"overwrite": true});
                }                
            }
        """
        params = {
            "permissionList": list(map(lambda obj: {
                "id": obj.id(),
                "name": obj.name(),
                "allowed_actions": obj.allowedActions(),
                "denied_actions": obj.deniedActions(),
            }, objList))
        }
        self._db.transaction(
            collections={"write": ["permission"]},
            action=actionFunction,
            params=params,
        )

    @debugLogger
    def deletePermission(self, obj: Permission, tokenData: TokenData = None):
        try:
            self._deletePermissions(objList=[obj])
        except Exception as e:
            print(e)
            self.permissionById(obj.id())
            logger.debug(
                f"[{PermissionRepositoryImpl.deletePermission.__qualname__}] Object could not be found exception for permission id: {obj.id()}"
            )
            raise ObjectCouldNotBeDeletedException(f"permission id: {obj.id()}")

    def _deletePermissions(self, objList: List[Permission]):
        actionFunction = """
            function (params) {                                            
                let db = require('@arangodb').db;
                let idList = params['permissionIdList'];
                db.permission.removeByKeys(idList);
                // Delete from the 'for' collection
                for (let index in idList) {
                    db.for.removeByExample({_from: `permission/${idList[index]}`});
                }
                // Delete from the 'has' collection
                for (let index in idList) {
                    db.has.removeByExample({_to: `permission/${idList[index]}`});
                }
            }
        """
        params = {
            "permissionIdList": list(map(lambda obj: obj.id(), objList))
        }
        self._db.transaction(
            collections={"write": ["permission", "for", "has"]},
            action=actionFunction,
            params=params,
        )
        from src.domain_model.policy.PolicyRepository import PolicyRepository
        policyRepo: PolicyRepository = AppDi.instance.get(PolicyRepository)
        policyRepo.deleteRolesTreesCache()

    @debugLogger
    def permissionByName(self, name: str) -> Permission:
        aql = """
            FOR d IN permission
                FILTER d.name == @name
                RETURN d
        """

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PermissionRepositoryImpl.permissionByName.__qualname__}] {name}"
            )
            raise PermissionDoesNotExistException(name)

        return Permission.createFrom(
            id=result[0]["id"],
            name=result[0]["name"],
            allowedActions=result[0]["allowed_actions"],
        )

    @debugLogger
    def permissionById(self, id: str) -> Permission:
        aql = """
            FOR d IN permission
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
                f"[{PermissionRepositoryImpl.permissionById.__qualname__}] permission id: {id}"
            )
            raise PermissionDoesNotExistException(f"permission id: {id}")

        return Permission.createFrom(
            id=result[0]["id"],
            name=result[0]["name"],
            allowedActions=result[0]["allowed_actions"] if 'allowed_actions' in result[0] else [],
            deniedActions=result[0]["denied_actions"] if 'denied_actions' in result[0] else [],
        )

    @debugLogger
    def permissions(
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

        result = self._policyService.permissionsByTokenData(
            tokenData, roleAccessPermissionData, sortData
        )

        if result is None or len(result["items"]) == 0:
            return {"items": [], "totalItemCount": 0}
        items = result["items"]
        totalItemCount = len(items)
        items = items[resultFrom : resultFrom + resultSize]
        objectItems = []
        for x in items:
            allowedActions = x["allowed_actions"] if "allowed_actions" in x else []
            deniedActions = x["denied_actions"] if "denied_actions" in x else []
            objectItems.append(
                Permission.createFrom(
                    id=x["id"],
                    name=x["name"],
                    allowedActions=allowedActions,
                    deniedActions=deniedActions,
                )
            )
        return {"items": objectItems, "totalItemCount": totalItemCount}
