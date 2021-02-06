"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleToResourceAccessGranted, "CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_GRANTED.value", "message", "event")
"""


class RoleToResourceAccessGranted(DomainEvent):
    def __init__(self, role: Role, resource: Resource):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_TO_RESOURCE_ACCESS_GRANTED.value)
        self._data = {'role_id': role.id(), 'resource_id': resource.id()}
