"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.permission.Permission import Permission

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__PermissionUpdated, "CommonEventConstant.PERMISSION_UPDATED.value", "message", "event")
"""


class PermissionUpdated(DomainEvent):
    def __init__(self, oldPermission: Permission, newPermission: Permission):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.PERMISSION_UPDATED.value
        )
        self._data = {"old": oldPermission.toMap(), "new": newPermission.toMap()}
