"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import (
    RequestedAuthzObject,
    RequestedAuthzObjectEnum,
)
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import (
    PermissionContext,
    PermissionContextConstant,
)
from src.domain_model.permission_context.PermissionContextRepository import (
    PermissionContextRepository,
)
from src.domain_model.permission_context.PermissionContextService import (
    PermissionContextService,
)
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.PermissionContextDataRequest import (
    PermissionContextDataRequest,
)
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import (
    ResourceTypeContextDataRequest,
)
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.ProcessBulkDomainException import ProcessBulkDomainException
from src.domain_model.token.TokenService import TokenService
from src.domain_model.util.DomainModelAttributeValidator import DomainModelAttributeValidator
from src.resource.logging.decorator import debugLogger


class PermissionContextApplicationService:
    def __init__(
        self,
        permissionContextRepository: PermissionContextRepository,
        authzService: AuthorizationService,
        permissionContextService: PermissionContextService,
    ):
        self._permissionContextRepository = permissionContextRepository
        self._authzService: AuthorizationService = authzService
        self._permissionContextService = permissionContextService

    @debugLogger
    def newId(self):
        return PermissionContext.createFrom().id()

    @debugLogger
    def createPermissionContext(
        self,
        id: str = None,
        type: str = "",
        data: dict = None,
        objectOnly: bool = False,
        token: str = "",
    ):
        data = {} if data is None else data
        obj: PermissionContext = self.constructObject(id=id, type=type, data=data)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.CREATE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value
            ),
            tokenData=tokenData,
        )
        return self._permissionContextService.createPermissionContext(
            obj=obj, objectOnly=objectOnly, tokenData=tokenData
        )

    @debugLogger
    def updatePermissionContext(
        self, id: str, type: str = "", data: dict = None, token: str = ""
    ):
        data = {} if data is None else data
        obj: PermissionContext = self.constructObject(id=id, type=type, data=data)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._permissionContextRepository.permissionContextById(id=obj.id())
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.UPDATE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value
            ),
            requestedObject=RequestedAuthzObject(
                objType=RequestedAuthzObjectEnum.PERMISSION_CONTEXT, obj=resource
            ),
            tokenData=tokenData,
        )
        self._permissionContextService.updatePermissionContext(
            oldObject=resource, newObject=obj, tokenData=tokenData
        )

    @debugLogger
    def deletePermissionContext(self, id: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._permissionContextRepository.permissionContextById(id=id)
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.DELETE,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value
            ),
            requestedObject=RequestedAuthzObject(
                objType=RequestedAuthzObjectEnum.PERMISSION_CONTEXT, obj=resource
            ),
            tokenData=tokenData,
        )
        self._permissionContextService.deletePermissionContext(
            obj=resource, tokenData=tokenData
        )

    @debugLogger
    def bulkCreate(self, objListParams: List[dict], token: str = ""):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                DomainModelAttributeValidator.validate(domainModelObject=self.constructObject(skipValidation=True),
                                                       attributeDictionary=objListParamsItem)
                objList.append(
                    self.constructObject(id=objListParamsItem["permission_context_id"], type=objListParamsItem["type"], data=objListParamsItem["data"]))
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionContextService.bulkCreate(objList=objList)
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
                objList.append(self.constructObject(id=objListParamsItem["permission_context_id"], skipValidation=True))
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionContextService.bulkDelete(objList=objList)
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
                oldObject: PermissionContext = self._permissionContextRepository.permissionContextById(id=objListParamsItem["permission_context_id"])
                newObject = self.constructObject(id=objListParamsItem["permission_context_id"], type=objListParamsItem["type"], data=objListParamsItem["data"], _sourceObject=oldObject)
                objList.append((newObject, oldObject), )
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._permissionContextService.bulkUpdate(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def permissionContextById(self, id: str, token: str = ""):
        permissionContext = self._permissionContextRepository.permissionContextById(
            id=id
        )
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.PERMISSION_CONTEXT.value
            ),
            requestedObject=RequestedAuthzObject(obj=permissionContext),
            tokenData=tokenData,
        )
        return permissionContext

    @debugLogger
    def permissionContexts(
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
        return self._permissionContextRepository.permissionContexts(
            tokenData=tokenData,
            roleAccessPermissionData=roleAccessPermissionData,
            resultFrom=resultFrom,
            resultSize=resultSize,
            order=order,
        )

    @debugLogger
    def constructObject(
        self, id: str = None, type: str = "", data: dict = None, skipValidation: bool = False,
    ) -> PermissionContext:
        return PermissionContext.createFrom(id=id, type=type, data=data, skipValidation=skipValidation)

    @debugLogger
    def constructObject(
            self,
            id: str = None,
            type: str = "",
            data: dict = None,
            _sourceObject: PermissionContext = None,
            skipValidation: bool = False,
    ) -> PermissionContext:
        if _sourceObject is not None:
            return PermissionContext.createFrom(
                id=id,
                type=type if type is not None else _sourceObject.type(),
                data=data if data is not None else _sourceObject.data(),
                skipValidation=skipValidation,
            )
        else:
            return PermissionContext.createFrom(
            id=id, type=type, data=data, skipValidation=skipValidation,
        )