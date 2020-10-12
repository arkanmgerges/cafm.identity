"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.resource_type.ResourceType import ResourceType


class ResourceTypeUpdated(DomainEvent):
    def __init__(self, oldResourceType: ResourceType, newResourceType: ResourceType):
        super().__init__(id=str(uuid4()), name='resource_type_updated')
        self._data = {'old': oldResourceType.toMap(), 'new': newResourceType.toMap()}

