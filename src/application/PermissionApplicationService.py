"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import (
    RequestedAuthzObject,
    RequestedAuthzObjectEnum,
)
from src.domain_model.permission.Permission import Permission, PermissionAction
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission.PermissionService import PermissionService
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
)
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.PermissionContextDataRequest import (
    PermissionContextDataRequest,
)
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.ProcessBulkDomainException import ProcessBulkDomainException
from src.domain_model.token.TokenService import TokenService
from src.domain_model.util.DomainModelAttributeValidator import DomainModelAttributeValidator
from src.resource.logging.decorator import debugLogger


class PermissionApplicationService:
    def __init__(
        self,
        permissionRepository: PermissionRepository,
        authzService: AuthorizationService,
        permissionService: PermissionService,
    ):
        self._permissionRepository = permissionRepository
        self._authzService: AuthorizationService = authzService
        self._permissionService = permissionService

    @debugLogger
    def newId(self):
        return Permission.createFrom().id()

    @debugLogger
    def createPermission(
        self,
        id: str = None,
        name: str = "",
        allowedActions: List[str] = None,
        deniedActions: List[str] = None,
        objectOnly: bool = False,
        token: str = "",
    ):
        obj: Permission = self.constructObject(
            id=id, name=name, allowedActions=allowedActions, deniedActions=deniedActions
        )
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.CREATE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION.value
            ),
            tokenData=tokenData,
        )
        return self._permissionService.createPermission(
            obj=obj, objectOnly=objectOnly, tokenData=tokenData
        )

    @debugLogger
    def updatePermission(
        self,
        id: str,
        name: str,
        token: str = "",
        allowedActions: List[str] = None,
        deniedActions: List[str] = None,
    ):
        obj: Permission = self.constructObject(
            id=id, name=name, allowedActions=allowedActions, deniedActions=deniedActions
        )
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        permission = self._permissionRepository.permissionById(id=obj.id())
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.UPDATE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION.value
            ),
            requestedObject=RequestedAuthzObject(
                objType=RequestedAuthzObjectEnum.PERMISSION, obj=permission
            ),
            tokenData=tokenData,
        )
        self._permissionService.updatePermission(
            oldObject=permission, newObject=obj, tokenData=tokenData
        )

    @debugLogger
    def deletePermission(self, id: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        permission = self._permissionRepository.permissionById(id=id)
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.DELETE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION.value
            ),
            requestedObject=RequestedAuthzObject(
                objType=RequestedAuthzObjectEnum.PERMISSION, obj=permission
            ),
            tokenData=tokenData,
        )
        self._permissionService.deletePermission(obj=permission, tokenData=tokenData)

    @debugLogger
    def bulkCreate(self, objListParams: List[dict], token: str = ""):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                DomainModelAttributeValidator.validate(domainModelObject=self.constructObject(skipValidation=True),
                                                       attributeDictionary=objListParamsItem)
                objList.append(
                    self.constructObject(id=objListParamsItem["permission_id"], name=objListParamsItem["name"],
                                         allowedActions=objListParamsItem['allowed_actions'],
                                         deniedActions=objListParamsItem['denied_actions']))
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionService.bulkCreate(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def bulkDelete(self, objListParams: List[dict], token: str = ""):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                DomainModelAttributeValidator.validate(domainModelObject=self.constructObject(skipValidation=True),
                                                       attributeDictionary=objListParamsItem)
                objList.append(self.constructObject(id=objListParamsItem["permission_id"], skipValidation=True))
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionService.bulkDelete(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def bulkUpdate(self, objListParams: List[dict], token: str = ""):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                DomainModelAttributeValidator.validate(domainModelObject=self.constructObject(skipValidation=True),
                                                       attributeDictionary=objListParamsItem)
                oldObject: Permission = self._permissionRepository.permissionById(id=objListParamsItem["permission_id"])
                newObject = self.constructObject(id=objListParamsItem["permission_id"],
                                                 name=objListParamsItem["name"], _sourceObject=oldObject)
                objList.append((newObject, oldObject), )
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionService.bulkUpdate(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def permissionByName(self, name: str, token: str = ""):
        permission = self._permissionRepository.permissionByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION.value
            ),
            requestedObject=RequestedAuthzObject(obj=permission),
            tokenData=tokenData,
        )
        return permission

    @debugLogger
    def permissionById(self, id: str, token: str = ""):
        permission = self._permissionRepository.permissionById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION.value
            ),
            requestedObject=RequestedAuthzObject(obj=permission),
            tokenData=tokenData,
        )
        return permission

    @debugLogger
    def permissions(
        self,
        resultFrom: int = 0,
        resultSize: int = 100,
        token: str = "",
        order: List[dict] = None,
    ) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        return self._permissionRepository.permissions(
            tokenData=tokenData,
            roleAccessPermissionData=roleAccessPermissionData,
            resultFrom=resultFrom,
            resultSize=resultSize,
            order=order,
        )

    @debugLogger
    def constructObject(
            self,
            id: str = None,
            name: str = "",
            allowedActions: List[str] = None,
            deniedActions: List[str] = None,
            _sourceObject: Permission = None, skipValidation: bool = False,
    ) -> Permission:
        if _sourceObject is not None:
            return Permission.createFrom(
            id=id,
                name=name if name is not None else _sourceObject.name(),
                allowedActions=allowedActions if allowedActions is not None else _sourceObject.allowedActions(),
                deniedActions=deniedActions if deniedActions is not None else _sourceObject.deniedActions(),
                skipValidation=skipValidation,
        )
        else:
            return Permission.createFrom(
            id=id, name=name, allowedActions=allowedActions, deniedActions=deniedActions, skipValidation=skipValidation,
        )
