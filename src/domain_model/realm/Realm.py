"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.Resource import Resource
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Realm(Resource, HasToMap):
    def __init__(
        self,
        id: str = None,
        name: str = None,
        realmType: str = None,
        skipValidation: bool = False,
    ):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type="realm")
        self._name = name
        self._realmType = realmType

    @classmethod
    def createFrom(
        cls,
        id: str = None,
        name: str = None,
        realmType: str = None,
        publishEvent: bool = False,
        skipValidation: bool = False,
        **_kwargs,
    ):
        logger.debug(
            f"[{Realm.createFrom.__qualname__}] - Create Realm with name: {name} and id: {id}"
        )
        realm = Realm(
            id=id,
            name=name,
            realmType=realmType,
            skipValidation=skipValidation,
        )
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.realm.RealmCreated import RealmCreated

            logger.debug(
                f"[{Realm.createFrom.__qualname__}] - Publish event for realm with name: {name} and id: {id}"
            )
            DomainPublishedEvents.addEventForPublishing(RealmCreated(realm))
        return realm

    @classmethod
    def createFromObject(
        cls, obj: "Realm", publishEvent: bool = False, generateNewId: bool = False
    ):
        logger.debug(f"[{Realm.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(
            id=id, name=obj.name(), realmType=obj.realmType(), publishEvent=publishEvent
        )

    def name(self) -> str:
        return self._name

    def realmType(self) -> str:
        return self._realmType

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if "name" in data and data["name"] != self._name:
            updated = True
            self._name = data["name"]
        if "realm_type" in data and data["realm_type"] != self._realmType:
            updated = True
            self._realmType = data["realm_type"]
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.realm.RealmDeleted import RealmDeleted

        DomainPublishedEvents.addEventForPublishing(RealmDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.realm.RealmUpdated import RealmUpdated

        DomainPublishedEvents.addEventForPublishing(RealmUpdated(old, self))

    def toMap(self) -> dict:
        return {
            "realm_id": self.id(),
            "name": self.name(),
            "realm_type": self.realmType(),
        }

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, Realm):
            raise NotImplementedError(
                f"other: {other} can not be compared with Realm class"
            )
        return (
            self.id() == other.id()
            and self.name() == other.name()
            and self.realmType() == other.realmType()
        )
