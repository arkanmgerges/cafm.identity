"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant, PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.ResourceRepository import ResourceRepository
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.resource.logging.decorator import debugLogger


class PolicyApplicationService:
    def __init__(self, roleRepository: RoleRepository, userRepository: UserRepository,
                 policyRepository: PolicyRepository,
                 policyControllerService: PolicyControllerService,
                 userGroupRepository: UserGroupRepository,
                 permissionRepository: PermissionRepository,
                 permissionContextRepository: PermissionContextRepository,
                 resourceRepository: ResourceRepository,
                 authzService: AuthorizationService):
        self._roleRepository = roleRepository
        self._userRepository = userRepository
        self._userGroupRepository = userGroupRepository
        self._permissionRepository = permissionRepository
        self._permissionContextRepository = permissionContextRepository
        self._policyRepository = policyRepository
        self._policyControllerService = policyControllerService
        self._resourceRepository = resourceRepository
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def assignRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value):
            role = self._roleRepository.roleById(id=roleId)
            user = self._userRepository.userById(id=userId)
            self._policyRepository.assignRoleToUser(role, user)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value):
            role = self._roleRepository.roleById(id=roleId)
            user = self._userRepository.userById(id=userId)
            self._policyRepository.revokeRoleFromUser(role, user)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def assignRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value):
            role = self._roleRepository.roleById(id=roleId)
            userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
            self._policyRepository.assignRoleToUserGroup(role, userGroup)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value):
            role = self._roleRepository.roleById(id=roleId)
            userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
            self._policyRepository.revokeRoleFromUserGroup(role, userGroup)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def assignUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value):
            user = self._userRepository.userById(id=userId)
            userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
            self._policyRepository.assignUserToUserGroup(user, userGroup)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value):
            user = self._userRepository.userById(id=userId)
            userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
            self._policyRepository.revokeUserFromUserGroup(user, userGroup)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def assignRoleToPermission(self, roleId: str = '',
                               permissionId: str = '',
                               token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value):
            role = self._roleRepository.roleById(id=roleId)
            permission = self._permissionRepository.permissionById(id=permissionId)
            self._policyRepository.assignRoleToPermission(role=role, permission=permission)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentRoleToPermission(self, roleId: str = '',
                                         permissionId: str = '',
                                         token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value):
            role = self._roleRepository.roleById(id=roleId)
            permission = self._permissionRepository.permissionById(id=permissionId)
            self._policyRepository.revokeAssignmentRoleToPermission(role=role, permission=permission)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def assignPermissionToPermissionContext(self, permissionId: str = '',
                                       permissionContextId: str = '',
                                       token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.ASSIGN.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_RESOURCE_TYPE.value):
            permission = self._permissionRepository.permissionById(id=permissionId)
            permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
            self._policyRepository.assignPermissionToPermissionContext(permission=permission, permissionContext=permissionContext)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentPermissionToPermissionContext(self, permissionId: str = '',
                                                 permissionContextId: str = '',
                                                 token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_RESOURCE_TYPE.value):
            permission = self._permissionRepository.permissionById(id=permissionId)
            permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
            self._policyRepository.revokeAssignmentPermissionToPermissionContext(permission=permission,
                                                                            permissionContext=permissionContext)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def provideAccessRoleToResource(self, roleId: str = '', resourceId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE.value):
            role = self._roleRepository.roleById(id=roleId)
            resource = self._resourceRepository.resourceById(id=resourceId)
            self._policyRepository.provideAccessRoleToResource(role, resource)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAccessRoleFromResource(self, roleId: str = '', resourceId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE.value):
            role = self._roleRepository.roleById(id=roleId)
            resource = self._resourceRepository.resourceById(id=resourceId)
            self._policyRepository.revokeAccessRoleFromResource(role, resource)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def assignResourceToResource(self, resourceSrcId: str = '', resourceDstId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE.value):
            resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
            resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
            self._policyControllerService.assignResourceToResource(resourceSrc=resourceSrc, resourceDst=resourceDst)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def revokeAssignmentResourceToResource(self, resourceSrcId: str = '', resourceDstId: str = '', token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.REVOKE.value,
                                        permissionContext=PermissionContextConstant.ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE.value):
            resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
            resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
            self._policyRepository.revokeAssignmentResourceToResource(resourceSrc=resourceSrc,
                                                                      resourceDst=resourceDst)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def roleByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.ROLE.value):
            return self._roleRepository.roleByName(name=name)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def roleById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.ROLE.value):
            return self._roleRepository.roleById(id=id)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def deleteRole(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        permissionContext=PermissionContextConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            self._roleRepository.deleteRole(role)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def updateRole(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        permissionContext=PermissionContextConstant.ROLE.value):
            role = self._roleRepository.roleById(id=id)
            role.update({'name': name})
            self._roleRepository.updateRole(role)
        else:
            raise UnAuthorizedException()

    @debugLogger
    def roles(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
              order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.ROLE.value):
            return {}
        else:
            raise UnAuthorizedException()
