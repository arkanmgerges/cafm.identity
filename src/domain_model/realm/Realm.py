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


class Realm:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False):
        realm = Realm(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.realm.RealmCreated import RealmCreated
            logger.debug(f'[{Realm.createFrom.__qualname__}] - Create Realm with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(RealmCreated(realm))
        return realm

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
        from src.domain_model.realm.RealmDeleted import RealmDeleted
        DomainEventPublisher.addEventForPublishing(RealmDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.realm.RealmUpdated import RealmUpdated
        DomainEventPublisher.addEventForPublishing(RealmUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, Realm):
            raise NotImplementedError(f'other: {other} is can not be compared with Realm class')
        return self.id() == other.id() and self.name() == other.name()