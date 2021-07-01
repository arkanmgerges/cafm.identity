"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission.Permission import PermissionAction, Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
    PermissionContext,
)
from src.domain_model.permission_context.PermissionContextRepository import (
    PermissionContextRepository,
)
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.policy.PolicyService import PolicyService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.PermissionContextDataRequest import (
    PermissionContextDataRequest,
)
from src.domain_model.resource.ResourceRepository import ResourceRepository
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.domain_model.resource.exception.InvalidAttributeException import (
    InvalidAttributeException,
)
from src.domain_model.resource.exception.ProcessBulkDomainException import (
    ProcessBulkDomainException,
)
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.domain_model.util.DomainModelAttributeValidator import (
    DomainModelAttributeValidator,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PolicyApplicationService:
    def __init__(
        self,
        roleRepository: RoleRepository,
        userRepository: UserRepository,
        policyRepository: PolicyRepository,
        policyControllerService: PolicyControllerService,
        userGroupRepository: UserGroupRepository,
        permissionRepository: PermissionRepository,
        permissionContextRepository: PermissionContextRepository,
        resourceRepository: ResourceRepository,
        policyService: PolicyService,
        authzService: AuthorizationService,
    ):
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
    def assignRoleToUser(self, roleId: str = "", userId: str = "", token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value
            ),
            tokenData=tokenData,
        )

        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._policyService.assignRoleToUser(role=role, user=user)

    @debugLogger
    def usersIncludeAccessRoles(self, token: str = None):
        tokenData = TokenService.tokenDataFromToken(token=token)
        return self._policyService.usersIncludeAccessRoles(tokenData=tokenData)

    @debugLogger
    def usersIncludeRoles(self, token: str = None):
        tokenData = TokenService.tokenDataFromToken(token=token)
        return self._policyService.usersIncludeRoles(tokenData=tokenData)

    @debugLogger
    def realmsIncludeUsersIncludeRoles(self, token: str = None):
        tokenData = TokenService.tokenDataFromToken(token=token)
        return self._policyService.realmsIncludeUsersIncludeRoles(tokenData=tokenData)

    @debugLogger
    def projectsIncludeRealmsIncludeUsersIncludeRoles(self, token: str = None):
        tokenData = TokenService.tokenDataFromToken(token=token)
        return self._policyService.projectsIncludeRealmsIncludeUsersIncludeRoles(tokenData=tokenData)

    @debugLogger
    def revokeRoleToUserAssignment(
        self, roleId: str = "", userId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._policyService.revokeRoleToUserAssignment(role=role, user=user)

    @debugLogger
    def assignRoleToUserGroup(
        self, roleId: str = "", userGroupId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER_GROUP.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyService.assignRoleToUserGroup(role, userGroup)

    @debugLogger
    def revokeAssignmentRoleToUserGroup(
        self, roleId: str = "", userGroupId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_USER_GROUP.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyService.revokeRoleToUserGroupAssignment(role, userGroup)

    @debugLogger
    def assignUserToUserGroup(
        self, userId: str = "", userGroupId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value
            ),
            tokenData=tokenData,
        )
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyService.assignUserToUserGroup(user, userGroup)

    @debugLogger
    def revokeAssignmentUserToUserGroup(
        self, userId: str = "", userGroupId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_USER_TO_USER_GROUP.value
            ),
            tokenData=tokenData,
        )
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._policyService.revokeUserToUserGroupAssignment(user, userGroup)

    @debugLogger
    def assignRoleToPermission(
        self, roleId: str = "", permissionId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._policyService.assignRoleToPermission(role=role, permission=permission)

    @debugLogger
    def revokeAssignmentRoleToPermission(
        self, roleId: str = "", permissionId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_ROLE_TO_PERMISSION.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._policyService.revokeRoleToPermissionAssignment(
            role=role, permission=permission
        )

    @debugLogger
    def assignPermissionToPermissionContext(
        self, permissionId: str = "", permissionContextId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT.value
            ),
            tokenData=tokenData,
        )
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(
            id=permissionContextId
        )
        self._policyService.assignPermissionToPermissionContext(
            permission=permission, permissionContext=permissionContext
        )

    @debugLogger
    def revokeAssignmentPermissionToPermissionContext(
        self, permissionId: str = "", permissionContextId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT.value
            ),
            tokenData=tokenData,
        )
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(
            id=permissionContextId
        )
        self._policyService.revokePermissionToPermissionContextAssignment(
            permission=permission, permissionContext=permissionContext
        )

    @debugLogger
    def bulkAssignPermissionToPermissionContext(
        self, objListParams: List[dict], token: str = ""
    ):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                if (
                    "permission_id" not in objListParamsItem
                    or "permission_context_id" not in objListParamsItem
                ):
                    raise InvalidAttributeException(
                        message=f'The needed parameters are: permission_id and permission_context_id. Received: {",".join(objListParamsItem)}'
                    )
                objList.append(
                    {
                        "permission": Permission.createFrom(
                            id=objListParamsItem["permission_id"], skipValidation=True
                        ),
                        "permission_context": PermissionContext.createFrom(
                            id=objListParamsItem["permission_context_id"],
                            skipValidation=True,
                        ),
                    }
                )
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._policyService.bulkAssignPermissionToPermissionContext(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def bulkRemovePermissionToPermissionContextAssignment(
        self, objListParams: List[dict], token: str = ""
    ):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                if (
                    "permission_id" not in objListParamsItem
                    or "permission_context_id" not in objListParamsItem
                ):
                    raise InvalidAttributeException(
                        message=f"The needed parameters are: permission_id and "
                        f'permission_context_id. Received: {",".join(objListParamsItem)}'
                    )
                objList.append(
                    {
                        "permission": Permission.createFrom(
                            id=objListParamsItem["permission_id"], skipValidation=True
                        ),
                        "permission_context": PermissionContext.createFrom(
                            id=objListParamsItem["permission_context_id"],
                            skipValidation=True,
                        ),
                    }
                )
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._policyService.bulkRemovePermissionToPermissionContextAssignment(
                objList=objList
            )
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    @debugLogger
    def bulkAssignRoleToPermission(
            self, objListParams: List[dict], token: str = ""
    ):
        objList = []
        exceptions = []
        for objListParamsItem in objListParams:
            try:
                if (
                        "role_id" not in objListParamsItem
                        or "permission_id" not in objListParamsItem
                ):
                    raise InvalidAttributeException(
                        message=f'The needed parameters are: role_id and permission_id. Received: {",".join(objListParamsItem)}'
                    )
                objList.append(
                    {
                        "role": Role.createFrom(
                            id=objListParamsItem["role_id"],
                            skipValidation=True,
                        ),
                        "permission": Permission.createFrom(
                            id=objListParamsItem["permission_id"], skipValidation=True
                        ),
                    }
                )
            except DomainModelException as e:
                exceptions.append({"reason": {"message": e.message, "code": e.code}})
        _ = TokenService.tokenDataFromToken(token=token)
        try:
            self._policyService.bulkAssignRoleToPermission(objList=objList)
            if len(exceptions) > 0:
                raise ProcessBulkDomainException(messages=exceptions)
        except DomainModelException as e:
            exceptions.append({"reason": {"message": e.message, "code": e.code}})
            raise ProcessBulkDomainException(messages=exceptions)

    def _constructPermissionByIdOnly(self, id: str):
        return Permission.createFrom(id=id, skipValidation=True)

    def _constructPermissionContextByIdOnly(self, id: str):
        return PermissionContext.createFrom(id=id, skipValidation=True)

    @debugLogger
    def grantAccessRoleToResource(
        self, roleId: str = "", resourceId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.GRANT,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ACCESS_ROLE_TO_RESOURCE.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._policyService.grantAccessRoleToResource(role, resource)

    @debugLogger
    def revokeAccessRoleFromResource(
        self, roleId: str = "", resourceId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ACCESS_ROLE_TO_RESOURCE.value
            ),
            tokenData=tokenData,
        )
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._policyService.revokeRoleToResourceAccess(role, resource)

    @debugLogger
    def assignResourceToResource(
        self, resourceSrcId: str = "", resourceDstId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.ASSIGN,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_RESOURCE_TO_RESOURCE.value
            ),
            tokenData=tokenData,
        )
        resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
        resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
        self._policyService.assignResourceToResource(
            resourceSrc=resourceSrc, resourceDst=resourceDst
        )

    @debugLogger
    def revokeAssignmentResourceToResource(
        self, resourceSrcId: str = "", resourceDstId: str = "", token: str = ""
    ):
        tokenData = TokenService.tokenDataFromToken(token=token)
        permissionAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=permissionAccessList,
            requestedPermissionAction=PermissionAction.REVOKE,
            requestedContextData=PermissionContextDataRequest(
                type=PermissionContextConstant.ASSIGNMENT_RESOURCE_TO_RESOURCE.value
            ),
            tokenData=tokenData,
        )
        resourceSrc = self._resourceRepository.resourceById(id=resourceSrcId)
        resourceDst = self._resourceRepository.resourceById(id=resourceDstId)
        self._policyService.revokeAssignmentResourceToResource(
            resourceSrc=resourceSrc, resourceDst=resourceDst
        )
