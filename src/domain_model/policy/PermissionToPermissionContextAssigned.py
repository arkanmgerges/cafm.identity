"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission_context.PermissionContext import PermissionContext

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__PermissionToPermissionContextAssigned, "CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED.value", "message", "event")
"""


class PermissionToPermissionContextAssigned(DomainEvent):
    def __init__(self, permission: Permission, permissionContext: PermissionContext):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED.value)
        self._data = {'permission_id': permission.id(), 'permission_context_id': permissionContext.id()}
