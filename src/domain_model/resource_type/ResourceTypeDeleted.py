"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.resource_type.ResourceType as ResourceType


class ResourceTypeDeleted(DomainEvent):
    def __init__(self, resourceType: ResourceType):
        super().__init__(id=str(uuid4()), name='resource_type_deleted')
        self._data = resourceType.toMap()
