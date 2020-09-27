"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.resourcetype.ResourceType import ResourceType


class ResourceTypeCreated(DomainEvent):
    def __init__(self, resourceType: ResourceType):
        super().__init__()
        self._data = json.dumps(resourceType.toMap())
