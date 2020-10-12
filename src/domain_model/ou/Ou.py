"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Ou:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False):
        ou = Ou(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.ou.OuCreated import OuCreated
            logger.debug(f'[{Ou.createFrom.__qualname__}] - Create Ou with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(OuCreated(ou))
        return ou

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
        from src.domain_model.ou.OuDeleted import OuDeleted
        DomainEventPublisher.addEventForPublishing(OuDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.ou.OuUpdated import OuUpdated
        DomainEventPublisher.addEventForPublishing(OuUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, Ou):
            raise NotImplementedError(f'other: {other} is can not be compared with Ou class')
        return self.id() == other.id() and self.name() == other.name()
