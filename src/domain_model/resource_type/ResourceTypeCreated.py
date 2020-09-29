"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.resource_type.ResourceType import ResourceType


class ResourceTypeCreated(DomainEvent):
    def __init__(self, resourceType: ResourceType):
        super().__init__(id=str(uuid4()), name='resource_type_created')
        self._data = resourceType.toMap()
