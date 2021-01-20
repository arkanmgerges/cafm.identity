"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User
from src.resource.logging.decorator import debugLogger


class PolicyService:
    def __init__(self, policyRepo: PolicyRepository):
        self._repo = policyRepo
        self._policyRepo = policyRepo

    @debugLogger
    def assignRoleToUser(self, role: Role, user: User):
        self._repo.assignRoleToUser(role, user)
        from src.domain_model.policy.RoleToUserAssigned import RoleToUserAssigned
        DomainPublishedEvents.addEventForPublishing(RoleToUserAssigned(role=role, user=user))

    @debugLogger
    def revokeRoleFromUser(self, role: Role, user: User):
        self._repo.revokeRoleFromUser(role, user)
        from src.domain_model.policy.RoleToUserAssignmentRevoked import RoleToUserAssignmentRevoked
        DomainPublishedEvents.addEventForPublishing(RoleToUserAssignmentRevoked(role=role, user=user))

    @debugLogger
    def assignResourceToResource(self, resourceSrc: Resource, resourceDst: Resource):
        self._repo.assignResourceToResource(resourceSrc=resourceSrc, resourceDst=resourceDst)
        from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
        if resourceSrc.type() == PermissionContextConstant.USER.value and \
                resourceDst.type() == PermissionContextConstant.REALM.value:
            from src.domain_model.policy.UserToRealmAssigned import UserToRealmAssigned
            DomainPublishedEvents.addEventForPublishing(UserToRealmAssigned(user=resourceSrc, realm=resourceDst))

    @debugLogger
    def revokeAssignmentResourceToResource(self, resourceSrc: Resource, resourceDst: Resource):
        self._repo.revokeAssignmentResourceToResource(resourceSrc=resourceSrc, resourceDst=resourceDst)
        from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
        if resourceSrc.type() == PermissionContextConstant.USER.value and \
                resourceDst.type() == PermissionContextConstant.REALM.value:
            from src.domain_model.policy.UserToRealmAssignmentRevoked import UserToRealmAssignmentRevoked
            DomainPublishedEvents.addEventForPublishing(
                UserToRealmAssignmentRevoked(user=resourceSrc, realm=resourceDst))
