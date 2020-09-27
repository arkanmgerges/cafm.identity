"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.role.Role import Role


class RoleCreated(DomainEvent):
    def __init__(self, role: Role):
        super().__init__()
        self._data = json.dumps(role.toMap())

