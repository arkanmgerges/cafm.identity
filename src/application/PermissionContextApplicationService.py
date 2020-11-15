"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContext, PermissionContextConstant
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.permission_context.PermissionContextService import PermissionContextService
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService


class PermissionContextApplicationService:
    def __init__(self, permissionContextRepository: PermissionContextRepository, authzService: AuthorizationService,
                 permissionContextService: PermissionContextService):
        self._permissionContextRepository = permissionContextRepository
        self._authzService: AuthorizationService = authzService
        self._permissionContextService = permissionContextService

    def createPermissionContext(self, id: str = '', data: dict = None, objectOnly: bool = False, token: str = ''):
        data = {} if data is None else data
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value),
                                        tokenData=tokenData)
        return self._permissionContextService.createPermissionContext(id=id, data=data, objectOnly=objectOnly,
                                                                      tokenData=tokenData)

    def updatePermissionContext(self, id: str, data: dict = None, token: str = ''):
        data = {} if data is None else data
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._permissionContextRepository.permissionContextById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value),
                                        resource=None,
                                        tokenData=tokenData)
        self._permissionContextService.updatePermissionContext(oldObject=resource,
                                                               newObject=PermissionContext.createFrom(id=id, data=data),
                                                               tokenData=tokenData)

    def deletePermissionContext(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._permissionContextRepository.permissionContextById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.PERMISSION_CONTEXT.value),
                                        resource=resource,
                                        tokenData=tokenData)
        self._permissionContextService.deletePermissionContext(permissionContext=resource, tokenData=tokenData)

    def permissionContextByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextByName(name=name)
        else:
            raise UnAuthorizedException()

    def permissionContextById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextById(id=id)
        else:
            raise UnAuthorizedException()

    def permissionContexts(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '',
                           order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextsByOwnedRoles(ownedRoles=ownedRoles,
                                                                                    resultFrom=resultFrom,
                                                                                    resultSize=resultSize,
                                                                                    order=order)
        else:
            raise UnAuthorizedException()
