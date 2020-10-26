"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from typing import List

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class PermissionAction(Enum):
    READ = 'read'
    WRITE = 'write'
    ASSIGN = 'assign'
    REVOKE = 'revoke'


class Permission(Resource):
    def __init__(self, id: str = None, name: str = '', allowedActions: List[str] = None):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type='permission')
        self._name = name
        self._allowedActions = [] if allowedActions is None else allowedActions

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False, allowedActions: List[str] = None):
        permission = Permission(id, name, allowedActions)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.permission.PermissionCreated import PermissionCreated
            logger.debug(
                f'[{Permission.createFrom.__qualname__}] - Create Permission with name: {name}, id: {id}, allowedActions: {allowedActions}')
            DomainEventPublisher.addEventForPublishing(PermissionCreated(permission))
        return permission

    def name(self) -> str:
        return self._name

    def allowedActions(self) -> List[str]:
        return self._allowedActions

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if 'allowedActions' in data and data['allowedActions'] != self._allowedActions:
            updated = True
            self._allowedActions = data['allowedActions']
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.permission.PermissionDeleted import PermissionDeleted
        DomainEventPublisher.addEventForPublishing(PermissionDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission.PermissionUpdated import PermissionUpdated
        DomainEventPublisher.addEventForPublishing(PermissionUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, Permission):
            raise NotImplementedError(f'other: {other} can not be compared with Permission class')
        return self.id() == other.id() and self.name() == other.name()
