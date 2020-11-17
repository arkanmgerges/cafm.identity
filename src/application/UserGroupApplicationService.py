"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.domain_model.user_group.UserGroupService import UserGroupService


class UserGroupApplicationService:
    def __init__(self, userGroupRepository: UserGroupRepository, authzService: AuthorizationService,
                 userGroupService: UserGroupService):
        self._userGroupRepository = userGroupRepository
        self._authzService: AuthorizationService = authzService
        self._userGroupService = userGroupService

    def createUserGroup(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='userGroup'),
                                        tokenData=tokenData)
        return self._userGroupService.createUserGroup(id=id, name=name, objectOnly=objectOnly, tokenData=tokenData)

    def updateUserGroup(self, id: str, name: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._userGroupRepository.userGroupById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='userGroup'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._userGroupService.updateUserGroup(oldObject=resource,
                                               newObject=UserGroup.createFrom(id=id, name=name), tokenData=tokenData)

    def deleteUserGroup(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._userGroupRepository.userGroupById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='userGroup'),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)
        self._userGroupService.deleteUserGroup(userGroup=resource, tokenData=tokenData)

    def userGroupByName(self, name: str, token: str = ''):
        resource = self._userGroupRepository.userGroupByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.USER_GROUP.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)

    def userGroupById(self, id: str, token: str = ''):
        resource = self._userGroupRepository.userGroupById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
                                        requestedPermissionAction=PermissionAction.READ,
                                        requestedContextData=ResourceTypeContextDataRequest(
                                            resourceType=PermissionContextConstant.USER_GROUP.value),
                                        requestedObject=RequestedAuthzObject(obj=resource),
                                        tokenData=tokenData)

    def userGroups(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
                   order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._userGroupRepository.userGroups(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                      resultFrom=resultFrom,
                                      resultSize=resultSize,
                                      order=order)
