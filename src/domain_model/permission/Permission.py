"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from typing import List

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class PermissionAction(Enum):
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    GRANT = 'grant'
    ASSIGN = 'assign'
    REVOKE = 'revoke'


class Permission:
    def __init__(self, id: str = None, name: str = '', allowedActions: List[str] = None,
                 deniedActions: List[str] = None):
        self._id = str(uuid4()) if id is None else id
        self._name = name
        self._allowedActions = [] if allowedActions is None else allowedActions
        self._deniedActions = [] if deniedActions is None else deniedActions

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False, allowedActions: List[str] = None,
                   deniedActions: List[str] = None):
        permission = Permission(id, name, allowedActions, deniedActions)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.permission.PermissionCreated import PermissionCreated
            logger.debug(
                f'[{Permission.createFrom.__qualname__}] - Create Permission with name: {name}, id: {id}, allowedActions: {allowedActions}, deniedActions: {deniedActions}')
            DomainPublishedEvents.addEventForPublishing(PermissionCreated(permission))
        return permission

    @classmethod
    def createFromObject(cls, obj: 'Permission', publishEvent: bool = False, generateNewId: bool = False):
        logger.debug(f'[{Permission.createFromObject.__qualname__}]')
        id = None if generateNewId else obj.id()
        return cls.createFrom(id=id, name=obj.name(), allowedActions=obj.allowedActions(),
                              deniedActions=obj.deniedActions(), publishEvent=publishEvent)

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def allowedActions(self) -> List[str]:
        return self._allowedActions if self._allowedActions is not [] else []

    def deniedActions(self) -> List[str]:
        return self._deniedActions if self._deniedActions is not [] else []

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if 'allowedActions' in data and data['allowedActions'] != self._allowedActions:
            updated = True
            self._allowedActions = data['allowedActions']
        if 'deniedActions' in data and data['deniedActions'] != self._deniedActions:
            updated = True
            self._deniedActions = data['deniedActions']
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.permission.PermissionDeleted import PermissionDeleted
        DomainPublishedEvents.addEventForPublishing(PermissionDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission.PermissionUpdated import PermissionUpdated
        DomainPublishedEvents.addEventForPublishing(PermissionUpdated(old, self))

    def toMap(self) -> dict:
        return {"permission_id": self.id(), "name": self.name(), "allowed_actions": self.allowedActions(),
                "denied_actions": self.deniedActions()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, Permission):
            raise NotImplementedError(f'other: {other} can not be compared with Permission class')
        return self.id() == other.id() and self.name() == other.name()
