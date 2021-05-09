"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from enum import Enum
from uuid import uuid4

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger


class PermissionContextConstant(Enum):
    REALM = "realm"
    OU = "ou"
    PROJECT = "project"
    RESOURCE_TYPE = "resource_type"
    RESOURCE_INSTANCE = "resource_instance"
    PERMISSION = "permission"
    PERMISSION_CONTEXT = "permission_context"
    USER = "user"
    USER_GROUP = "user_group"
    ASSIGNMENT_ROLE_TO_USER = "assignment:role_to_user"
    ASSIGNMENT_ROLE_TO_USER_GROUP = "assignment:role_to_user_group"
    ASSIGNMENT_USER_TO_USER_GROUP = "assignment:user_to_user_group"
    ASSIGNMENT_ROLE_TO_PERMISSION = "assignment:role_to_permission"
    ASSIGNMENT_RESOURCE_TO_RESOURCE = "assignment:resource_to_resource"
    ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT = (
        "assignment:permission_to_permission_context"
    )
    ACCESS_ROLE_TO_RESOURCE = "access:role_to_resource"
    RESOURCE_OWNERSHIP_OTHER = "resource_ownership:other"
    ALL_ROLES_TREES = "all_roles_trees"
    ROLE = "role"
    ALL = "*"


class PermissionContext(HasToMap):
    def __init__(
        self, id: str = None, type: str = "permission_context", data: dict = None, skipValidation: bool = False,
    ):
        self._id = str(uuid4()) if id is None else id
        self._type = type
        self._data = data if data is not None else {}

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return self._type

    @classmethod
    def createFrom(
        cls,
        id: str = None,
        type: str = "",
        data: dict = None,
        publishEvent: bool = False,
        skipValidation: bool = False,
    ):
        permissionContext = PermissionContext(id=id, type=type, data=data, skipValidation=skipValidation)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.permission_context.PermissionContextCreated import (
                PermissionContextCreated,
            )

            logger.debug(
                f"[{PermissionContext.createFrom.__qualname__}] - Create permission context with id = {id} and data = {data}"
            )
            DomainPublishedEvents.addEventForPublishing(
                PermissionContextCreated(permissionContext)
            )
        return permissionContext

    @classmethod
    def createFromObject(
        cls,
        obj: "PermissionContext",
        publishEvent: bool = False,
        generateNewId: bool = False,
    ):
        logger.debug(f"[{PermissionContext.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(
            id=id, type=obj.type(), data=obj.data(), publishEvent=publishEvent
        )

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if "data" in data:
            updated = True
            self._data = data["data"]
        if "type" in data:
            updated = True
            self._type = data["type"]
        if updated:
            self.publishUpdate(old)

    def data(self) -> dict:
        return self._data

    def publishDelete(self):
        from src.domain_model.permission_context.PermissionContextDeleted import (
            PermissionContextDeleted,
        )

        DomainPublishedEvents.addEventForPublishing(PermissionContextDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.permission_context.PermissionContextUpdated import (
            PermissionContextUpdated,
        )

        DomainPublishedEvents.addEventForPublishing(PermissionContextUpdated(old, self))

    def toMap(self) -> dict:
        return {
            "permission_context_id": self.id(),
            "type": self.type(),
            "data": self.data(),
        }

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, PermissionContext):
            raise NotImplementedError(
                f"other: {other} can not be compared with PermissionContext class"
            )
        return (
            self.id() == other.id()
            and self.type() == other.type()
            and self.data() == other.data()
        )
