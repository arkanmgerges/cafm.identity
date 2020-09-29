"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.resource_type.ResourceType import ResourceType


class ResourceTypeCreated(DomainEvent):
    def __init__(self, resourceType: ResourceType):
        super().__init__()
        self._data = json.dumps(resourceType.toMap())
