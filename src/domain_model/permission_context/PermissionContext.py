"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from uuid import uuid4

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger


class PermissionContextConstant(Enum):
    REALM = 'realm'
    OU = 'ou'
    PROJECT = 'project'
    RESOURCE_TYPE = 'resource_type'
    RESOURCE_INSTANCE = 'resource_instance'
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



class PermissionContext:
    def __init__(self, id: str = None, type: str = 'permission_context', data: dict = None):
        self._id = str(uuid4()) if id is None else id
        self._type = type
        self._data = data if data is not None else {}

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return self._type

    @classmethod
    def createFrom(cls, id: str = None, data: dict = None, publishEvent: bool = False):
        permissionContext = PermissionContext(id=id, data=data)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.permission_context.PermissionContextCreated import PermissionContextCreated
            logger.debug(
                f'[{PermissionContext.createFrom.__qualname__}] - Create permission context with id = {id} and data = {data}')
            DomainEventPublisher.addEventForPublishing(PermissionContextCreated(permissionContext))
        return permissionContext

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'data' in data:
            updated = True
            self._data = data['data']
        if updated:
            self.publishUpdate(old)

    def data(self):
        return self._data

    def publishDelete(self):
        from src.domain_model.permission_context.PermissionContextDeleted import PermissionContextDeleted
        DomainEventPublisher.addEventForPublishing(PermissionContextDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission_context.PermissionContextUpdated import PermissionContextUpdated
        DomainEventPublisher.addEventForPublishing(PermissionContextUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "data": self.data()}

    def __eq__(self, other):
        if not isinstance(other, PermissionContext):
            raise NotImplementedError(f'other: {other} can not be compared with PermissionContext class')
        return self.id() == other.id() and self.data() == other.data()