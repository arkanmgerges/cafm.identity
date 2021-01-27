"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.permission_context.PermissionContext as PermissionContext

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__PermissionContextDeleted, "Permission Context Deleted", "event", "message")
"""
class PermissionContextDeleted(DomainEvent):
    def __init__(self, permissionContext: PermissionContext):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PERMISSION_CONTEXT_DELETED.value)
        self._data = permissionContext.toMap()
