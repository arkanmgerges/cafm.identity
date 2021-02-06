"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.permission.Permission import Permission
from src.domain_model.role.Role import Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleToPermissionAssignmentRevoked, "CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED.value", "message", "event")
"""


class RoleToPermissionAssignmentRevoked(DomainEvent):
    def __init__(self, role: Role, permission: Permission):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED.value)
        self._data = {'role_id': role.id(), 'permission_id': permission.id()}
