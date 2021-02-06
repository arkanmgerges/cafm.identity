"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__ResourceToResourceAssigned, "CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNED.value", "message", "event")
"""


class ResourceToResourceAssigned(DomainEvent):
    def __init__(self, srcResource: Resource, dstResource: Resource):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.RESOURCE_TO_RESOURCE_ASSIGNED.value)
        self._data = {'src_resource_id': srcResource.id(), 'dst_resource_id': dstResource.id()}
