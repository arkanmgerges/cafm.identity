"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.permission.Permission import Permission


class PermissionCreated(DomainEvent):
    def __init__(self, permission: Permission):
        super().__init__()
        self._data = json.dumps(permission.toMap())

