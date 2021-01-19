"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User
from src.resource.logging.decorator import debugLogger
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents


class PolicyService:
    def __init__(self, policyRepo: PolicyRepository):
        self._repo = policyRepo
        self._policyRepo = policyRepo

    @debugLogger
    def assignRoleToUser(self, role: Role, user: User):
        self._repo.assignRoleToUser(role, user)
        from src.domain_model.policy.RoleToUserAssigned import RoleToUserAssigned
        DomainPublishedEvents.addEventForPublishing(RoleToUserAssigned(role=role, user=user))

    def revokeRoleFromUser(self, role: Role, user: User):
        self._repo.revokeRoleFromUser(role, user)
        from src.domain_model.policy.RoleToUserAssigned import RoleToUserAssigned
        DomainPublishedEvents.addEventForPublishing(RoleToUserRevoked(role=role, user=user))

