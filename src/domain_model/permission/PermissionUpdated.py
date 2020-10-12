"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.permission.Permission import Permission


class PermissionUpdated(DomainEvent):
    def __init__(self, oldPermission: Permission, newPermission: Permission):
        super().__init__(id=str(uuid4()), name='permission_updated')
        self._data = {'old': oldPermission.toMap(), 'new': newPermission.toMap()}

