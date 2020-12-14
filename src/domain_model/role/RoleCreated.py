"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.role.Role import Role


class RoleCreated(DomainEvent):
    def __init__(self, role: Role):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_CREATED.value)
        self._data = role.toMap()

