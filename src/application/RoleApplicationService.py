"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.role.RoleService import RoleService
from src.domain_model.token.TokenService import TokenService


class RoleApplicationService:
    def __init__(self, roleRepository: RoleRepository, authzService: AuthorizationService, roleService: RoleService):
        self._roleRepository = roleRepository
        self._authzService: AuthorizationService = authzService
        self._roleService = roleService

    def createRole(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='role'),
                                        tokenData=tokenData)
        return self._roleService.createRole(id=id, name=name, objectOnly=objectOnly, tokenData=tokenData)

    def updateRole(self, id: str, name: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        role = self._roleRepository.roleById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='role'),
                                        requestedObject=RequestedAuthzObject(obj=role),
                                        tokenData=tokenData)

        self._roleService.updateRole(oldObject=role, newObject=Role.createFrom(id=id, name=name), tokenData=tokenData)

    def deleteRole(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        role = self._roleRepository.roleById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='role'),
                                        requestedObject=RequestedAuthzObject(obj=role),
                                        tokenData=tokenData)

        self._roleService.deleteRole(role=role, tokenData=tokenData)

    def roleByName(self, name: str, token: str = ''):
        resource = self._roleRepository.roleByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.ROLE.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        return resource

    def roleById(self, id: str, token: str = ''):
        resource = self._roleRepository.roleById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.ROLE.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        return resource

    def roles(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
              order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._roleRepository.roles(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                          resultFrom=resultFrom,
                                          resultSize=resultSize,
                                          order=order)

    def rolesTrees(self, token: str = '') -> List[RoleAccessPermissionData]:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionDataList = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._roleRepository.rolesTrees(tokenData=tokenData, roleAccessPermissionDataList=roleAccessPermissionDataList)

    def roleTree(self, roleId: str = '', token: str = '') -> RoleAccessPermissionData:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._roleRepository.roleTree(tokenData=tokenData, roleId=roleId, roleAccessPermissionData=roleAccessPermissionData)
