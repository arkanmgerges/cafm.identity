"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger


class PermissionContextConstant(Enum):
    REALM = 'realm'
    OU = 'ou'
    PROJECT = 'project'
    RESOURCE_TYPE = 'permission_context'
    PERMISSION = 'permission'
    USER = 'user'
    USER_GROUP = 'user_group'
    ASSIGNMENT_ROLE_TO_USER = 'assignment:role_to_user'
    ASSIGNMENT_USER_TO_USER_GROUP = 'assignment:user_to_user_group'
    ASSIGNMENT_ROLE_TO_PERMISSION = 'assignment:role_to_permission'
    ASSIGNMENT_PERMISSION_TO_RESOURCE_TYPE = 'assignment:permission_to_permission_context'
    ASSIGNMENT_ROLE_TO_ACCESS_RESOURCE = 'assignment:role_to_access_resource'
    RESOURCE_OWNERSHIP_OTHER = 'resource_ownership:other'
    ROLE = 'role'
    ALL = '*'


class PermissionContext(Resource):
    def __init__(self, id: str = None, name=''):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type='permission_context')
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        permissionContext = PermissionContext(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.permission_context.PermissionContextCreated import PermissionContextCreated
            logger.debug(
                f'[{PermissionContext.createFrom.__qualname__}] - Create PermissionContext with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(PermissionContextCreated(permissionContext))
        return permissionContext

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
        from src.domain_model.permission_context.PermissionContextDeleted import PermissionContextDeleted
        DomainEventPublisher.addEventForPublishing(PermissionContextDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission_context.PermissionContextUpdated import PermissionContextUpdated
        DomainEventPublisher.addEventForPublishing(PermissionContextUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, PermissionContext):
            raise NotImplementedError(f'other: {other} can not be compared with PermissionContext class')
        return self.id() == other.id() and self.name() == other.name()