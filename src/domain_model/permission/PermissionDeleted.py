"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.permission.Permission as Permission


class PermissionDeleted(DomainEvent):
    def __init__(self, permission: Permission):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PERMISSION_DELETED.value)
        self._data = permission.toMap()
