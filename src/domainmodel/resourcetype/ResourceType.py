"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class ResourceType:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = True):
        resourceType = ResourceType(id, name)
        if publishEvent:
            from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
            from src.domainmodel.resourcetype.ResourceTypeCreated import ResourceTypeCreated
            DomainEventPublisher.addEventForPublishing(ResourceTypeCreated(resourceType))
        return resourceType

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
