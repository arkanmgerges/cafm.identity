"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.role.Role as Role


class RoleDeleted(DomainEvent):
    def __init__(self, role: Role):
        super().__init__(id=str(uuid4()), name='role_deleted')
        self._data = role.toMap()
