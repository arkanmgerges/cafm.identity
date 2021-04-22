"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.role.Role import Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleCreated, "CommonEventConstant.ROLE_CREATED.value", "message", "event")
"""


class RoleCreated(DomainEvent):
    def __init__(self, role: Role):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_CREATED.value)
        self._data = role.toMap()
