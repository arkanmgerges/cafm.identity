"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from typing import List, Callable

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.ResourceRepository import ResourceRepository
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.port_adapter.messaging.listener.db_persistence.handler.common.Util import Util
from src.resource.logging.logger import logger


class PolicyHandler(Handler):
    def __init__(self):
        import src.port_adapter.AppDi as AppDi
        self._eventConstants = [
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED.value,
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.ROLE_TO_USER_GROUP_ASSIGNED.value,
            CommonEventConstant.ROLE_TO_USER_GROUP_REVOKED.value,
            CommonEventConstant.ROLE_TO_USER_ASSIGNED.value,
            CommonEventConstant.ROLE_TO_USER_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.USER_TO_REALM_ASSIGNED.value,
            CommonEventConstant.USER_TO_REALM_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNED.value,
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNED.value,
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNED.value,
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED.value,
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_GRANTED.value,
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_REVOKED.value,
        ]
        self._repository: PolicyRepository = AppDi.instance.get(PolicyRepository)
        self._permissionRepository: PermissionRepository = AppDi.instance.get(PermissionRepository)
        self._permissionContextRepository: PermissionContextRepository = AppDi.instance.get(PermissionContextRepository)
        self._roleRepository: RoleRepository = AppDi.instance.get(RoleRepository)
        self._userRepository: UserRepository = AppDi.instance.get(UserRepository)
        self._userGroupRepository: UserGroupRepository = AppDi.instance.get(UserGroupRepository)
        self._resourceRepository: ResourceRepository = AppDi.instance.get(ResourceRepository)
        self._realmRepository: RealmRepository = AppDi.instance.get(RealmRepository)

    def canHandle(self, name: str) -> bool:
        return name in self._eventConstants

    def handleCommand(self, messageData: dict):
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{PolicyHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        # metadataDict = json.loads(metadata)
        #
        # if 'token' not in metadataDict:
        #     raise UnAuthorizedException()

        result = self.execute(name, **dataDict)
        return {'data': result, 'metadata': metadata}

    def execute(self, event, *args, **kwargs):
        funcSwitcher = {
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED.value: self._assignPermissionToPermissionContext,
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNMENT_REVOKED.value: self._revokePermissionToPermissionContextAssignment,
            CommonEventConstant.ROLE_TO_USER_GROUP_ASSIGNED.value: self._assignRoleToUserGroup,
            CommonEventConstant.ROLE_TO_USER_GROUP_REVOKED.value: self._revokeRoleToUserGroupAssignment,
            CommonEventConstant.ROLE_TO_USER_ASSIGNED.value: self._assignRoleToUser,
            CommonEventConstant.ROLE_TO_USER_ASSIGNMENT_REVOKED.value: self._revokeRoleToUserAssignment,
            CommonEventConstant.USER_TO_REALM_ASSIGNED.value: self._assignUserToRealm,
            CommonEventConstant.USER_TO_REALM_ASSIGNMENT_REVOKED.value: self._revokeUserToRealmAssignment,
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNED.value: self._assignResourceToResource,
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNMENT_REVOKED.value: self._revokeResourceToResourceAssignment,
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNED.value: self._assignUserToUserGroup,
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNMENT_REVOKED.value: self._revokeUserToUserGroupAssignment,
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNED.value: self._assignRoleToPermission,
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED.value: self._revokeRoleToPermissionAssignment,
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_GRANTED.value: self._grantRoleToResourceAccess,
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_REVOKED.value: self._revokeRoleToResourceAccess,
        }

        argSwitcher = {
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_USER_GROUP_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_USER_GROUP_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_USER_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_USER_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.USER_TO_REALM_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.USER_TO_REALM_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.USER_TO_USER_GROUP_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_GRANTED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
            CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_REVOKED.value: lambda: Util.snakeCaseToLowerCameCaseDict(
                kwargs),
        }
        func = funcSwitcher.get(event, None)
        if func is not None:
            # Execute the function with the arguments
            return func(*args, **(argSwitcher.get(event))())
        return None

    def _assignPermissionToPermissionContext(self, *_args, permissionId: str, permissionContextId: str):
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
        self._repository.assignPermissionToPermissionContext(permission=permission, permissionContext=permissionContext)
        return None

    def _revokePermissionToPermissionContextAssignment(self, *_args, permissionId: str, permissionContextId: str):
        permission = self._permissionRepository.permissionById(id=permissionId)
        permissionContext = self._permissionContextRepository.permissionContextById(id=permissionContextId)
        self._repository.revokePermissionToPermissionContextAssignment(permission=permission,
                                                                       permissionContext=permissionContext)
        return None

    def _assignRoleToUserGroup(self, *_args, roleId: str, userGroupId: str):
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._repository.assignRoleToUserGroup(role=role, userGroup=userGroup)
        return None

    def _revokeRoleToUserGroupAssignment(self, *_args, roleId: str, userGroupId: str):
        role = self._roleRepository.roleById(id=roleId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._repository.revokeRoleFromUserGroup(role=role, userGroup=userGroup)
        return None

    def _assignRoleToUser(self, *_args, roleId: str, userId: str):
        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._repository.assignRoleToUser(role=role, user=user)
        return None

    def _revokeRoleToUserAssignment(self, *_args, roleId: str, userId: str):
        role = self._roleRepository.roleById(id=roleId)
        user = self._userRepository.userById(id=userId)
        self._repository.revokeRoleFromUser(role=role, user=user)
        return None

    def _assignUserToRealm(self, *_args, userId: str, realmId: str):
        user = self._resourceRepository.resourceById(id=userId)
        realm = self._resourceRepository.resourceById(id=realmId)
        self._repository.assignResourceToResource(resourceSrc=user, resourceDst=realm)
        return None

    def _revokeUserToRealmAssignment(self, *_args, userId: str, realmId: str):
        user = self._resourceRepository.resourceById(id=userId)
        realm = self._resourceRepository.resourceById(id=realmId)
        self._repository.revokeAssignmentResourceToResource(resourceSrc=user, resourceDst=realm)
        return None

    def _assignResourceToResource(self, *_args, srcResourceId: str, dstResourceId: str):
        src = self._resourceRepository.resourceById(id=srcResourceId)
        dst = self._resourceRepository.resourceById(id=dstResourceId)
        self._repository.assignResourceToResource(resourceSrc=src, resourceDst=dst)
        return None

    def _revokeResourceToResourceAssignment(self, *_args, srcResourceId: str, dstResourceId: str):
        src = self._resourceRepository.resourceById(id=srcResourceId)
        dst = self._resourceRepository.resourceById(id=dstResourceId)
        self._repository.revokeAssignmentResourceToResource(resourceSrc=src, resourceDst=dst)
        return None

    def _assignUserToUserGroup(self, *_args, userId: str, userGroupId: str):
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._repository.assignUserToUserGroup(user=user, userGroup=userGroup)
        return None

    def _revokeUserToUserGroupAssignment(self, *_args, userId: str, userGroupId: str):
        user = self._userRepository.userById(id=userId)
        userGroup = self._userGroupRepository.userGroupById(id=userGroupId)
        self._repository.assignUserToUserGroup(user=user, userGroup=userGroup)
        return None

    def _assignRoleToPermission(self, *_args, roleId: str, permissionId: str):
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._repository.assignRoleToPermission(role=role, permission=permission)
        return None

    def _revokeRoleToPermissionAssignment(self, *_args, roleId: str, permissionId: str):
        role = self._roleRepository.roleById(id=roleId)
        permission = self._permissionRepository.permissionById(id=permissionId)
        self._repository.revokeRoleToPermissionAssignment(role=role, permission=permission)
        return None

    def _grantRoleToResourceAccess(self, *_args, roleId: str, resourceId: str):
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._repository.grantAccessRoleToResource(role=role, resource=resource)
        return None

    def _revokeRoleToResourceAccess(self, *_args, roleId: str, resourceId: str):
        role = self._roleRepository.roleById(id=roleId)
        resource = self._resourceRepository.resourceById(id=resourceId)
        self._repository.revokeRoleToResourceAccess(role=role, resource=resource)
        return None

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
