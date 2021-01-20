"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.policy.PolicyService import PolicyService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.PermissionContextDataRequest import PermissionContextDataRequest
from src.domain_model.resource.ResourceRepository import ResourceRepository
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.token.TokenService import TokenService
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
                 policyService: PolicyService,
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
        self._policyService: PolicyService = policyService

    @debugLogger
    def assignRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value),
                                        tokenData=tokenData)

        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._policyService.assignRoleToUser(role=role, user=user)

    @debugLogger
    def revokeAssignmentRoleToUser(self, roleId: str = '', userId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._policyService.revokeRoleFromUser(role=role, user=user)

    @debugLogger
    def assignRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER_GROUP.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyRepository.assignRoleToUserGroup(role, userGroup)

    @debugLogger
    def revokeAssignmentRoleToUserGroup(self, roleId: str = '', userGroupId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER_GROUP.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyRepository.revokeRoleFromUserGroup(role, userGroup)

    @debugLogger
    def assignUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value),
                                        tokenData=tokenData)
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyRepository.assignUserToUserGroup(user, userGroup)

    @debugLogger
    def revokeAssignmentUserToUserGroup(self, userId: str = '', userGroupId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value),
                                        tokenData=tokenData)
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyRepository.revokeUserFromUserGroup(user, userGroup)

    @debugLogger
    def assignRoleToPermission(self, roleId: str = '',
                               permissionId: str = '',
                               token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._policyRepository.assignRoleToPermission(role=role, permission=permission)

    @debugLogger
    def revokeAssignmentRoleToPermission(self, roleId: str = '',
                                         permissionId: str = '',
                                         token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._policyRepository.revokeAssignmentRoleToPermission(role=role, permission=permission)

    @debugLogger
    def assignPermissionToPermissionContext(self, permissionId: str = '',
                                            permissionContextId: str = '',
                                            token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT.value),
                                        tokenData=tokenData)
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
        self._policyRepository.assignPermissionToPermissionContext(permission=permission,
                                                                   permissionContext=permissionContext)

    @debugLogger
    def revokeAssignmentPermissionToPermissionContext(self, permissionId: str = '',
                                                      permissionContextId: str = '',
                                                      token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT.value),
                                        tokenData=tokenData)
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
        self._policyRepository.revokeAssignmentPermissionToPermissionContext(permission=permission,
                                                                             permissionContext=permissionContext)

    @debugLogger
    def grantAccessRoleToResource(self, roleId: str = '', resourceId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.GRANT,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ACCESS_ROLE_TO_RESOURCE.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._policyRepository.grantAccessRoleToResource(role, resource)

    @debugLogger
    def revokeAccessRoleFromResource(self, roleId: str = '', resourceId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ACCESS_ROLE_TO_RESOURCE.value),
                                        tokenData=tokenData)
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._policyRepository.revokeAccessRoleFromResource(role, resource)

    @debugLogger
    def assignResourceToResource(self, resourceSrcId: str = '', resourceDstId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.ASSIGN,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_RESOURCE_TO_RESOURCE.value),
                                        tokenData=tokenData)
        resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
        resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
        self._policyService.assignResourceToResource(resourceSrc=resourceSrc, resourceDst=resourceDst)

    @debugLogger
    def revokeAssignmentResourceToResource(self, resourceSrcId: str = '', resourceDstId: str = '', token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=permissionAccessList,
                                        requestedPermissionAction=PermissionAction.REVOKE,
                                        requestedContextData=PermissionContextDataRequest(
                                            type=PermissionContextConstant.ASSIGNMENT_RESOURCE_TO_RESOURCE.value),
                                        tokenData=tokenData)
        resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
        resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
        self._policyService.revokeAssignmentResourceToResource(resourceSrc=resourceSrc, resourceDst=resourceDst)
