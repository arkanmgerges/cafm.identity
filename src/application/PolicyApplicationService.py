"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


class PolicyApplicationService:
    def __init__(self, roleRepository: RoleRepository, userRepository: UserRepository,
                 policyRepository: PolicyRepository,
                 userGroupRepository: UserGroupRepository,
                 permissionRepository: PermissionRepository,
                 resourceTypeRepository: ResourceTypeRepository,
                 authzService: AuthorizationService):
        self._roleRepository = roleRepository
        self._userRepository = userRepository
        self._userGroupRepository = userGroupRepository
        self._permissionRepository = permissionRepository
        self._resourceTypeRepository = resourceTypeRepository
        self._policyRepository = policyRepository
        self._authzService: AuthorizationService = authzService

    def assignRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_USER.value):
                role = self._roleRepository.roleById(id=roleId)
                user = self._userRepository.userById(id=userId)
                self._policyRepository.assignRoleToUser(role, user)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def revokeAssignmentRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_USER.value):
                role = self._roleRepository.roleById(id=roleId)
                user = self._userRepository.userById(id=userId)
                self._policyRepository.revokeRoleFromUser(role, user)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def assignRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_USER.value):
                role = self._roleRepository.roleById(id=roleId)
                userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
                self._policyRepository.assignRoleToUserGroup(role, userGroup)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def revokeAssignmentRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_USER.value):
                role = self._roleRepository.roleById(id=roleId)
                userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
                self._policyRepository.revokeRoleFromUserGroup(role, userGroup)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def assignUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_USER_TO_USER_GROUP.value):
                user = self._userRepository.userById(id=userId)
                userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
                self._policyRepository.assignUserToUserGroup(user, userGroup)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def revokeAssignmentUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_USER_TO_USER_GROUP.value):
                user = self._userRepository.userById(id=userId)
                userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
                self._policyRepository.revokeUserFromUserGroup(user, userGroup)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def assignRoleToPermissionForResourceType(self, roleId: str = '',
                                              permissionId: str = '',
                                              resourceTypeId: str = '',
                                              token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_PERMISSION_FOR_RESOURCE_TYPE.value):
                role = self._roleRepository.roleById(id=roleId)
                permission = self._permissionRepository.permissionById(id=permissionId)
                resourceType = self._resourceTypeRepository.resourceTypeById(id=resourceTypeId)
                self._policyRepository.assignRoleToPermissionForResourceType(role=role,
                                                                             permission=permission,
                                                                             resourceType=resourceType)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def revokeRoleFromPermissionForResourceType(self, roleId: str = '',
                                                permissionId: str = '',
                                                resourceTypeId: str = '',
                                                token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                            resourceType=ResourceTypeConstant.ASSIGNMENT_ROLE_TO_PERMISSION_FOR_RESOURCE_TYPE.value):
                role = self._roleRepository.roleById(id=roleId)
                permission = self._permissionRepository.permissionById(id=permissionId)
                resourceType = self._resourceTypeRepository.resourceTypeById(id=resourceTypeId)
                self._policyRepository.revokeRoleFromPermissionForResourceType(role=role,
                                                                               permission=permission,
                                                                               resourceType=resourceType)
            else:
                raise UnAuthorizedException()
        finally:
            pass

    def roleByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.roleByName(name=name)
        else:
            raise UnAuthorizedException()

    def roleById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.roleById(id=id)
        else:
            raise UnAuthorizedException()

    def deleteRole(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            self._roleRepository.deleteRole(role)
        else:
            raise UnAuthorizedException()

    def updateRole(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            role.update({'name': name})
            self._roleRepository.updateRole(role)
        else:
            raise UnAuthorizedException()

    def roles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '',
              order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.ROLE.value):
            return self._roleRepository.rolesByOwnedRoles(ownedRoles=ownedRoles,
                                                          resultFrom=resultFrom,
                                                          resultSize=resultSize,
                                                          order=order)
        else:
            raise UnAuthorizedException()
