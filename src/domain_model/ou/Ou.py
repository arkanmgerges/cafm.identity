"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger
from uuid import uuid4


class Ou(Resource, HasToMap):
    def __init__(self, id: str = None, name=None):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type="ou")
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name=None, publishEvent: bool = False, **_kwargs):
        ou = Ou(id, name)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.ou.OuCreated import OuCreated

            logger.debug(
                f"[{Ou.createFrom.__qualname__}] - Create Ou with name = {name} and id = {id}"
            )
            DomainPublishedEvents.addEventForPublishing(OuCreated(ou))
        return ou

    @classmethod
    def createFromObject(
        cls, obj: "Ou", publishEvent: bool = False, generateNewId: bool = False
    ):
        logger.debug(f"[{Ou.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(id=id, name=obj.name(), publishEvent=publishEvent)

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if "name" in data and data["name"] != self._name:
            updated = True
            self._name = data["name"]
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.ou.OuDeleted import OuDeleted

        DomainPublishedEvents.addEventForPublishing(OuDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.ou.OuUpdated import OuUpdated

        DomainPublishedEvents.addEventForPublishing(OuUpdated(old, self))

    def toMap(self) -> dict:
        return {"ou_id": self.id(), "name": self.name()}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, Ou):
            raise NotImplementedError(
                f"other: {other} can not be compared with Ou class"
            )
        return self.id() == other.id() and self.name() == other.name()
