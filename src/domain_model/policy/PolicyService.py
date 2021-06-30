"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Tuple

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user.User import User
from src.domain_model.user_group.UserGroup import UserGroup
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PolicyService:
    def __init__(self, policyRepo: PolicyRepository):
        self._repo = policyRepo

    @debugLogger
    def assignRoleToUser(self, role: Role, user: User):
        from src.domain_model.policy.RoleToUserAssigned import RoleToUserAssigned

        DomainPublishedEvents.addEventForPublishing(
            RoleToUserAssigned(role=role, user=user)
        )
        self._repo.assignRoleToUser(role=role, user=user)

    @debugLogger
    def revokeRoleFromUser(self, role: Role, user: User):
        from src.domain_model.policy.RoleToUserAssignmentRevoked import (
            RoleToUserAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToUserAssignmentRevoked(role=role, user=user)
        )
        self._repo.revokeRoleFromUser(role=role, user=user)

    @debugLogger
    def assignRoleToPermission(self, role: Role, permission: Permission):
        from src.domain_model.policy.RoleToPermissionAssigned import (
            RoleToPermissionAssigned,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToPermissionAssigned(role=role, permission=permission)
        )
        self._repo.assignRoleToPermission(role=role, permission=permission)

    @debugLogger
    def revokeRoleToPermissionAssignment(self, role: Role, permission: Permission):
        from src.domain_model.policy.RoleToPermissionAssignmentRevoked import (
            RoleToPermissionAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToPermissionAssignmentRevoked(role=role, permission=permission)
        )
        self._repo.revokeRoleToPermissionAssignment(role=role, permission=permission)

    @debugLogger
    def bulkAssignPermissionToPermissionContext(self, objList: List[dict]):
        self._repo.bulkAssignPermissionToPermissionContext(objList=objList)
        for objListItem in objList:
            from src.domain_model.policy.PermissionToPermissionContextAssigned import (
                PermissionToPermissionContextAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                PermissionToPermissionContextAssigned(
                    permission=objListItem["permission"],
                    permissionContext=objListItem["permission_context"],
                )
            )

    @debugLogger
    def bulkRemovePermissionToPermissionContextAssignment(self, objList: List[dict]):
        self._repo.bulkRemovePermissionToPermissionContextAssignment(objList=objList)
        for objListItem in objList:
            from src.domain_model.policy.PermissionToPermissionContextAssignmentRevoked import (
                PermissionToPermissionContextAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                PermissionToPermissionContextAssignmentRevoked(
                    permission=objListItem["permission"],
                    permissionContext=objListItem["permission_context"],
                )
            )

    @debugLogger
    def bulkAssignRoleToPermission(self, objList: List[dict]):
        self._repo.bulkAssignRoleToPermission(objList=objList)
        for objListItem in objList:
            from src.domain_model.policy.RoleToPermissionAssigned import (
                RoleToPermissionAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                RoleToPermissionAssigned(
                    role=objListItem["role"],
                    permission=objListItem["permission"],
                )
            )

    @debugLogger
    def grantAccessRoleToResource(self, role: Role, resource: Resource):
        from src.domain_model.policy.RoleToResourceAccessGranted import (
            RoleToResourceAccessGranted,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToResourceAccessGranted(role=role, resource=resource)
        )
        if resource.type() == "realm":
            from src.domain_model.policy.RoleToRealmAssigned import RoleToRealmAssigned

            DomainPublishedEvents.addEventForPublishing(
                RoleToRealmAssigned(role=role, realm=resource)
            )
        elif resource.type() == "project":
            from src.domain_model.policy.RoleToProjectAssigned import (
                RoleToProjectAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                RoleToProjectAssigned(role=role, project=resource)
            )
        self._repo.grantAccessRoleToResource(role=role, resource=resource)

    @debugLogger
    def revokeRoleToResourceAccess(self, role: Role, resource: Resource):
        from src.domain_model.policy.RoleToResourceAccessRevoked import (
            RoleToResourceAccessRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToResourceAccessRevoked(role=role, resource=resource)
        )
        if resource.type() == "realm":
            from src.domain_model.policy.RoleToRealmAssignmentRevoked import (
                RoleToRealmAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                RoleToRealmAssignmentRevoked(role=role, realm=resource)
            )
        elif resource.type() == "project":
            from src.domain_model.policy.RoleToProjectAssignmentRevoked import (
                RoleToProjectAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                RoleToProjectAssignmentRevoked(role=role, project=resource)
            )
        self._repo.revokeRoleToResourceAccess(role=role, resource=resource)

    @debugLogger
    def assignUserToUserGroup(self, user: User, userGroup: UserGroup):
        from src.domain_model.policy.UserToUserGroupAssigned import (
            UserToUserGroupAssigned,
        )

        DomainPublishedEvents.addEventForPublishing(
            UserToUserGroupAssigned(user=user, userGroup=userGroup)
        )
        self._repo.assignUserToUserGroup(user=user, userGroup=userGroup)

    @debugLogger
    def revokeUserToUserGroupAssignment(self, user: User, userGroup: UserGroup):
        from src.domain_model.policy.UserToUserGroupAssignmentRevoked import (
            UserToUserGroupAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            UserToUserGroupAssignmentRevoked(user=user, userGroup=userGroup)
        )
        self._repo.revokeUserFromUserGroup(user=user, userGroup=userGroup)

    @debugLogger
    def assignRoleToUserGroup(self, role: Role, userGroup: UserGroup):
        from src.domain_model.policy.RoleToUserGroupAssigned import (
            RoleToUserGroupAssigned,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToUserGroupAssigned(role=role, userGroup=userGroup)
        )
        self._repo.assignRoleToUserGroup(role=role, userGroup=userGroup)

    @debugLogger
    def revokeRoleToUserGroupAssignment(self, role: Role, userGroup: UserGroup):
        from src.domain_model.policy.RoleToUserGroupAssignmentRevoked import (
            RoleToUserGroupAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToUserGroupAssignmentRevoked(role=role, userGroup=userGroup)
        )
        self._repo.revokeRoleFromUserGroup(role=role, userGroup=userGroup)

    @debugLogger
    def revokeRoleToUserAssignment(self, role: Role, user: User):
        from src.domain_model.policy.RoleToUserAssignmentRevoked import (
            RoleToUserAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            RoleToUserAssignmentRevoked(role=role, user=user)
        )
        self._repo.revokeRoleFromUser(role=role, user=user)

    @debugLogger
    def assignResourceToResource(self, resourceSrc: Resource, resourceDst: Resource):
        from src.domain_model.permission_context.PermissionContext import (
            PermissionContextConstant,
        )

        if (
            resourceSrc.type() == PermissionContextConstant.USER.value
            and resourceDst.type() == PermissionContextConstant.REALM.value
        ):
            from src.domain_model.policy.UserToRealmAssigned import UserToRealmAssigned

            DomainPublishedEvents.addEventForPublishing(
                UserToRealmAssigned(user=resourceSrc, realm=resourceDst)
            )
        elif (
            resourceSrc.type() == PermissionContextConstant.PROJECT.value
            and resourceDst.type() == PermissionContextConstant.REALM.value
        ):
            from src.domain_model.policy.ProjectToRealmAssigned import (
                ProjectToRealmAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                ProjectToRealmAssigned(project=resourceSrc, realm=resourceDst)
            )
        elif (
            resourceSrc.type() == PermissionContextConstant.ROLE.value
            and resourceDst.type() == PermissionContextConstant.PROJECT.value
        ):
            from src.domain_model.policy.RoleToProjectAssigned import (
                RoleToProjectAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                RoleToProjectAssigned(role=resourceSrc, project=resourceDst)
            )
        else:
            from src.domain_model.policy.ResourceToResourceAssigned import (
                ResourceToResourceAssigned,
            )

            DomainPublishedEvents.addEventForPublishing(
                ResourceToResourceAssigned(
                    srcResource=resourceSrc, dstResource=resourceDst
                )
            )
        self._repo.assignResourceToResource(
            resourceSrc=resourceSrc, resourceDst=resourceDst
        )

    @debugLogger
    def revokeAssignmentResourceToResource(
        self, resourceSrc: Resource, resourceDst: Resource
    ):
        from src.domain_model.permission_context.PermissionContext import (
            PermissionContextConstant,
        )

        if (
            resourceSrc.type() == PermissionContextConstant.USER.value
            and resourceDst.type() == PermissionContextConstant.REALM.value
        ):
            from src.domain_model.policy.UserToRealmAssignmentRevoked import (
                UserToRealmAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                UserToRealmAssignmentRevoked(user=resourceSrc, realm=resourceDst)
            )
        elif (
            resourceSrc.type() == PermissionContextConstant.PROJECT.value
            and resourceDst.type() == PermissionContextConstant.REALM.value
        ):
            from src.domain_model.policy.ProjectToRealmAssignmentRevoked import (
                ProjectToRealmAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                ProjectToRealmAssignmentRevoked(project=resourceSrc, realm=resourceDst)
            )
        else:
            from src.domain_model.policy.ResourceToResourceAssignmentRevoked import (
                ResourceToResourceAssignmentRevoked,
            )

            DomainPublishedEvents.addEventForPublishing(
                ResourceToResourceAssignmentRevoked(
                    srcResource=resourceSrc, dstResource=resourceDst
                )
            )
        self._repo.revokeAssignmentResourceToResource(
            resourceSrc=resourceSrc, resourceDst=resourceDst
        )

    @debugLogger
    def assignPermissionToPermissionContext(
        self, permission: Permission, permissionContext: PermissionContext
    ):
        from src.domain_model.policy.PermissionToPermissionContextAssigned import (
            PermissionToPermissionContextAssigned,
        )

        DomainPublishedEvents.addEventForPublishing(
            PermissionToPermissionContextAssigned(
                permission=permission, permissionContext=permissionContext
            )
        )
        self._repo.assignPermissionToPermissionContext(
            permission=permission, permissionContext=permissionContext
        )

    @debugLogger
    def revokePermissionToPermissionContextAssignment(
        self, permission: Permission, permissionContext: PermissionContext
    ):
        from src.domain_model.policy.PermissionToPermissionContextAssignmentRevoked import (
            PermissionToPermissionContextAssignmentRevoked,
        )

        DomainPublishedEvents.addEventForPublishing(
            PermissionToPermissionContextAssignmentRevoked(
                permission=permission, permissionContext=permissionContext
            )
        )
        self._repo.revokePermissionToPermissionContextAssignment(
            permission=permission, permissionContext=permissionContext
        )


    @debugLogger
    def usersIncludeAccessRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        return self._repo.usersIncludeAccessRoles(tokenData=tokenData)

    @debugLogger
    def usersIncludeRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        return self._repo.usersIncludeRoles(tokenData=tokenData)

    @debugLogger
    def realmsIncludeUsersIncludeRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        return self._repo.realmsIncludeUsersIncludeRoles(tokenData=tokenData)