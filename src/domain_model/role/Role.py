"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Role(Resource):
    def __init__(self, id: str = None, name='', ownedBy: str = 'super_admin'):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type='role')
        self._name = name
        self._creator = ownedBy

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False, ownedBy: str = 'super_admin'):
        role = Role(id, name, ownedBy)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.role.RoleCreated import RoleCreated
            logger.debug(
                f'[{Role.createFrom.__qualname__}] - Create Role with name: {name} and id: {id}, creator: {ownedBy}')
            DomainEventPublisher.addEventForPublishing(RoleCreated(role))
        return role

    def name(self) -> str:
        return self._name

    def publishDelete(self):
        from src.domain_model.role.RoleDeleted import RoleDeleted
        DomainEventPublisher.addEventForPublishing(RoleDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.role.RoleUpdated import RoleUpdated
        DomainEventPublisher.addEventForPublishing(RoleUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if updated:
            self.publishUpdate(old)

    def __eq__(self, other):
        if not isinstance(other, Role):
            raise NotImplementedError(f'other: {other} can not be compared with Role class')
        return self.id() == other.id() and self.name() == other.name()
