"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.role.Role as Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleDeleted, "Role Deleted", "event", "message")
"""
class RoleDeleted(DomainEvent):
    def __init__(self, role: Role):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_DELETED.value)
        self._data = role.toMap()
