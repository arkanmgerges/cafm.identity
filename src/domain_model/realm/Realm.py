"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Realm(Resource):
    def __init__(self, id: str = None, name=''):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId, type='realm')
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        logger.debug(f'[{Realm.createFrom.__qualname__}] - Create Realm with name: {name} and id: {id}')
        realm = Realm(id, name)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.realm.RealmCreated import RealmCreated
            logger.debug(f'[{Realm.createFrom.__qualname__}] - Publish event for realm with name: {name} and id: {id}')
            DomainPublishedEvents.addEventForPublishing(RealmCreated(realm))
        return realm

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
        DomainPublishedEvents.addEventForPublishing(RealmDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.realm.RealmUpdated import RealmUpdated
        DomainPublishedEvents.addEventForPublishing(RealmUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, Realm):
            raise NotImplementedError(f'other: {other} can not be compared with Realm class')
        return self.id() == other.id() and self.name() == other.name()