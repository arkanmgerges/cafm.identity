"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.permission_context.PermissionContext import PermissionContext

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__PermissionContextUpdated, "CommonEventConstant.PERMISSION_CONTEXT_UPDATED.value", "message", "event")
"""


class PermissionContextUpdated(DomainEvent):
    def __init__(
        self,
        oldPermissionContext: PermissionContext,
        newPermissionContext: PermissionContext,
    ):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.PERMISSION_CONTEXT_UPDATED.value
        )
        self._data = {
            "old": oldPermissionContext.toMap(),
            "new": newPermissionContext.toMap(),
        }
