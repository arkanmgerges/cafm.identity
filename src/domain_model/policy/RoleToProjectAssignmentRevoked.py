"""
@author: Mohammad M. mmdii<mmdii@develoop.run>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleToProjectAssignmentRevoked, "CommonEventConstant.ROLE_TO_PROJECT_ASSIGNMENT_REVOKED.value", "message", "event")
"""


class RoleToProjectAssignmentRevoked(DomainEvent):
    def __init__(self, role: Role, project: Resource):
        super().__init__(
            id=str(uuid4()),
            name=CommonEventConstant.ROLE_TO_PROJECT_ASSIGNMENT_REVOKED.value,
        )
        self._data = {"role_id": role.id(), "project_id": project.id()}
