"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
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
                                        resource=resource,
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
                                        resource=resource,
                                        tokenData=tokenData)
        self._userGroupService.deleteUserGroup(userGroup=resource, tokenData=tokenData)

    def userGroupByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.USER_GROUP.value):
            return self._userGroupRepository.userGroupByName(name=name)
        else:
            raise UnAuthorizedException()

    def userGroupById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.USER_GROUP.value):
            return self._userGroupRepository.userGroupById(id=id)
        else:
            raise UnAuthorizedException()

    def userGroups(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '',
                   order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.USER_GROUP.value):
            return self._userGroupRepository.userGroupsByOwnedRoles(ownedRoles=ownedRoles,
                                                                    resultFrom=resultFrom,
                                                                    resultSize=resultSize,
                                                                    order=order)
        else:
            raise UnAuthorizedException()
