"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.role.Role import Role


class RoleUpdated(DomainEvent):
    def __init__(self, oldRole: Role, newRole: Role):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_UPDATED.value)
        self._data = {'old': oldRole.toMap(), 'new': newRole.toMap()}

