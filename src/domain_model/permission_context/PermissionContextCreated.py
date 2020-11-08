"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.permission_context.PermissionContext import PermissionContext


class PermissionContextCreated(DomainEvent):
    def __init__(self, permissionContext: PermissionContext):
        super().__init__(id=str(uuid4()), name='permission_context_created')
        self._data = permissionContext.toMap()
