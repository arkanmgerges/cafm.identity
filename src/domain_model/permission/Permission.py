"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Permission:
    def __init__(self, id: str = str(uuid4()), name='', allowedActions=None):
        self._id = id
        self._name = name
        self._allowedActions = [] if allowedActions is None else allowedActions

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False, allowedActions: List[str] = None):
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

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
