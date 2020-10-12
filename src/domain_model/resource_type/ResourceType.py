"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum
from uuid import uuid4

from src.resource.logging.logger import logger


class ResourceTypeConstant(Enum):
    REALM = 'realm'
    OU = 'ou'
    PROJECT = 'project'
    RESOURCE_TYPE = 'resource_type'
    PERMISSION = 'permission'
    USER = 'user'
    USER_GROUP = 'user_group'
    ROLE = 'role'
    ALL = '*'


class ResourceType:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False):
        resourceType = ResourceType(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.resource_type.ResourceTypeCreated import ResourceTypeCreated
            logger.debug(
                f'[{ResourceType.createFrom.__qualname__}] - Create ResourceType with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(ResourceTypeCreated(resourceType))
        return resourceType

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
