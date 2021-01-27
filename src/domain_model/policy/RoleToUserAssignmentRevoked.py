"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleToUserAssignmentRevoked, "Role to User Assignment Revoked", "event", "message")
"""
class RoleToUserAssignmentRevoked(DomainEvent):
    def __init__(self, role: Role, user: User):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_TO_USER_ASSIGNMENT_REVOKED.value)
        self._data = {'role_id': role.id(), 'user_id': user.id()}
