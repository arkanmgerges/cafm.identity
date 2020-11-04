"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger


class ResourceTypeConstant(Enum):
    REALM = 'realm'
    OU = 'ou'
    PROJECT = 'project'
    RESOURCE_TYPE = 'resource_type'
    PERMISSION = 'permission'
    USER = 'user'
    USER_GROUP = 'user_group'
    ASSIGNMENT_ROLE_TO_USER = 'assignment:role_to_user'
    ASSIGNMENT_USER_TO_USER_GROUP = 'assignment:user_to_user_group'
    ASSIGNMENT_ROLE_TO_PERMISSION = 'assignment:role_to_permission'
    ASSIGNMENT_PERMISSION_TO_RESOURCE_TYPE = 'assignment:permission_to_resource_type'
    ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE = 'assignment:role_to_access_resource'
    RESOURCE_OWNERSHIP_OTHER = 'resource_ownership:other'
    ROLE = 'role'
    ALL = '*'


class ResourceType(Resource):
    def __init__(self, id: str = None, name=''):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type='resource_type')
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        resourceType = ResourceType(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.resource_type.ResourceTypeCreated import ResourceTypeCreated
            logger.debug(
                f'[{ResourceType.createFrom.__qualname__}] - Create ResourceType with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(ResourceTypeCreated(resourceType))
        return resourceType

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.resource_type.ResourceTypeDeleted import ResourceTypeDeleted
        DomainEventPublisher.addEventForPublishing(ResourceTypeDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.resource_type.ResourceTypeUpdated import ResourceTypeUpdated
        DomainEventPublisher.addEventForPublishing(ResourceTypeUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, ResourceType):
            raise NotImplementedError(f'other: {other} can not be compared with ResourceType class')
        return self.id() == other.id() and self.name() == other.name()