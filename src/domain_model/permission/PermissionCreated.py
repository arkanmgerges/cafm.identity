"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.permission.Permission import Permission

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__PermissionCreated, "Permission Created", "event", "message")
"""
class PermissionCreated(DomainEvent):
    def __init__(self, permission: Permission):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PERMISSION_CREATED.value)
        self._data = permission.toMap()

