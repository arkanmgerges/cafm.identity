"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.role.Role import Role


class RoleForProjectAccessCreated(DomainEvent):
    def __init__(self, role: Role, projectId: str):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_FOR_PROJECT_ACCESS_CREATED.value)
        self._data = role.toMap()
        self._data['project_id'] = projectId
