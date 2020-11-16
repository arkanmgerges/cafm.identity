"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject, RequestedAuthzObjectEnum
from src.domain_model.permission.Permission import Permission, PermissionAction
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission.PermissionService import PermissionService
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService


class PermissionApplicationService:
    def __init__(self, permissionRepository: PermissionRepository, authzService: AuthorizationService,
                 permissionService: PermissionService):
        self._permissionRepository = permissionRepository
        self._authzService: AuthorizationService = authzService
        self._permissionService = permissionService

    def createPermission(self, id: str = '', name: str = '', allowedActions: List[str] = None,
                         deniedActions: List[str] = None, objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='permission'),
                                        tokenData=tokenData)
        return self._permissionService.createPermission(id=id, name=name, allowedActions=allowedActions,
                                                        deniedActions=deniedActions, objectOnly=objectOnly,
                                                        tokenData=tokenData)

    def updatePermission(self, id: str, name: str, token: str = '', allowedActions: List[str] = None,
                         deniedActions: List[str] = None, ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        permission = self._permissionRepository.permissionById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='permission'),
                                        requestedObject=RequestedAuthzObject(objType=RequestedAuthzObjectEnum.PERMISSION, obj=permission),
                                        tokenData=tokenData)

        self._permissionService.updatePermission(oldObject=permission,
                                                 newObject=Permission.createFrom(id=id, name=name,
                                                                                 allowedActions=allowedActions,
                                                                                 deniedActions=deniedActions),
                                                 tokenData=tokenData)

    def deletePermission(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        permission = self._permissionRepository.permissionById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='permission'),
                                        requestedObject=RequestedAuthzObject(objType=RequestedAuthzObjectEnum.PERMISSION, obj=permission),
                                        tokenData=tokenData)
        self._permissionService.deletePermission(permission=permission, tokenData=tokenData)

    def permissionByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.PERMISSION.value):
            return self._permissionRepository.permissionByName(name=name)
        else:
            raise UnAuthorizedException()

    def permissionById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.PERMISSION.value):
            return self._permissionRepository.permissionById(id=id)
        else:
            raise UnAuthorizedException()

    def permissions(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
                    order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._permissionRepository.permissions(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                      resultFrom=resultFrom,
                                      resultSize=resultSize,
                                      order=order)
