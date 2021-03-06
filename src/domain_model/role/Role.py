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


class Role(Resource, HasToMap):
    def __init__(self, id: str = None, name="", title: str = "", skipValidation: bool = False):
        anId = str(uuid4()) if id is None or id == "" else id
        super().__init__(id=anId, type="role")
        self._name = name
        self._title = title if title is not None else title

    @classmethod
    def createFrom(
        cls, id: str = None, name="", title: str = "", publishEvent: bool = False, skipValidation: bool = False,
            **_kwargs,
    ):
        role = Role(id, name, title, skipValidation=skipValidation)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.role.RoleCreated import RoleCreated

            logger.debug(
                f"[{Role.createFrom.__qualname__}] - Create Role with name: {name} and id: {id}"
            )
            DomainPublishedEvents.addEventForPublishing(RoleCreated(role))
        return role

    @classmethod
    def createFromObject(
        cls, obj: "Role", publishEvent: bool = False, generateNewId: bool = False
    ):
        logger.debug(f"[{Role.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(
            id=id, name=obj.name(), title=obj.title(), publishEvent=publishEvent
        )

    @classmethod
    def createFromObjectForProjectAccess(
        cls, obj: "Role", publishEvent: bool = False, generateNewId: bool = False, projectId: str = ''
    ):
        logger.debug(f"[{Role.createFromObject.__qualname__}]")

        from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
        from src.domain_model.role.RoleForProjectAccessCreated import RoleForProjectAccessCreated

        role = Role( obj.id(), obj.name(), obj.title(), skipValidation=False)

        result = cls.createFrom(
            id= obj.id(), name=obj.name(), title=obj.title(), publishEvent=publishEvent
        )
        DomainPublishedEvents.addEventForPublishing(RoleForProjectAccessCreated(role, projectId))
        return result

    @classmethod
    def createFromObjectForRealmAccess(
        cls, obj: "Role", publishEvent: bool = False, generateNewId: bool = False, realmId: str = ''
    ):
        logger.debug(f"[{Role.createFromObject.__qualname__}]")

        from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
        from src.domain_model.role.RoleForRealmAccessCreated import RoleForRealmAccessCreated

        role = Role( obj.id(), obj.name(), obj.title(), skipValidation=False)

        result = cls.createFrom(
            id= obj.id(), name=obj.name(), title=obj.title(), publishEvent=publishEvent
        )
        DomainPublishedEvents.addEventForPublishing(RoleForRealmAccessCreated(role, realmId))
        return result

    @classmethod
    def createFromObjectForUserAccess(
        cls, obj: "Role", publishEvent: bool = False, generateNewId: bool = False, userId: str = ''
    ):
        logger.debug(f"[{Role.createFromObject.__qualname__}]")

        from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
        from src.domain_model.role.RoleForUserAccessCreated import RoleForUserAccessCreated

        role = Role( obj.id(), obj.name(), obj.title(), skipValidation=False)

        result = cls.createFrom(
            id= obj.id(), name=obj.name(), title=obj.title(), publishEvent=publishEvent
        )
        DomainPublishedEvents.addEventForPublishing(RoleForUserAccessCreated(role, userId))
        return result

    def name(self) -> str:
        return self._name

    def title(self) -> str:
        return self._title

    def publishDelete(self):
        from src.domain_model.role.RoleDeleted import RoleDeleted

        DomainPublishedEvents.addEventForPublishing(RoleDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.role.RoleUpdated import RoleUpdated

        DomainPublishedEvents.addEventForPublishing(RoleUpdated(old, self))

    def toMap(self) -> dict:
        return {
            "role_id": self.id(),
            "type": self.type(),
            "name": self.name(),
            "title": self.title(),
        }

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if "name" in data and data["name"] != self._name:
            updated = True
            self._name = data["name"]
        if "title" in data and data["title"] != self._title:
            updated = True
            self._title = data["title"]
        if updated:
            self.publishUpdate(old)

    def __eq__(self, other):
        if not isinstance(other, Role):
            raise NotImplementedError(
                f"other: {other} can not be compared with Role class"
            )
        return (
            self.id() == other.id()
            and self.name() == other.name()
            and self.title() == other.title()
        )
