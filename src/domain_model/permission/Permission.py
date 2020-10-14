"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from typing import List

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Permission:
    def __init__(self, id: str = None, name='', allowedActions=None):
        self._id = str(uuid4()) if id is None else id
        self._name = name
        self._allowedActions = [] if allowedActions is None else allowedActions

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False, allowedActions: List[str] = None):
        permission = Permission(id, name, allowedActions)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.permission.PermissionCreated import PermissionCreated
            logger.debug(f'[{Permission.createFrom.__qualname__}] - Create Permission with name: {name}, id: {id}, allowedActions: {allowedActions}')
            DomainEventPublisher.addEventForPublishing(PermissionCreated(permission))
        return permission

    def id(self) -> str:
        return self._id

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
        from src.domain_model.permission.PermissionDeleted import PermissionDeleted
        DomainEventPublisher.addEventForPublishing(PermissionDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission.PermissionUpdated import PermissionUpdated
        DomainEventPublisher.addEventForPublishing(PermissionUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, Permission):
            raise NotImplementedError(f'other: {other} is can not be compared with Permission class')
        return self.id() == other.id() and self.name() == other.name()