"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import re
from copy import copy
from uuid import uuid4

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.InvalidValueException import (
    InvalidValueException,
)
from src.resource.logging.logger import logger


class User(Resource, HasToMap):
    ONE_TIME_PASSWORD_TAG = "###ABC_ZYX_1_TIME_PASS"

    def __init__(
        self,
        id: str = None,
        email: str = "",
        password: str = "",
        skipValidation: bool = False,
    ):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type="user")

        if not skipValidation:
            self._validateEmail(email)
        self._email = email
        self._password = password

    @classmethod
    def createFrom(
        cls,
        id: str = None,
        email: str = "",
        password: str = "",
        publishEvent: bool = False,
        skipValidation: bool = False,
        **_kwargs,
    ):
        logger.debug(f"[{User.createFrom.__qualname__}] - with name {email}")
        user = User(
            id=id, email=email, password=password, skipValidation=skipValidation
        )
        if publishEvent:
            logger.debug(
                f"[{User.createFrom.__qualname__}] - publish UserCreated event"
            )
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.user.UserCreated import UserCreated

            DomainPublishedEvents.addEventForPublishing(UserCreated(user))
        return user

    @classmethod
    def createFromObject(
        cls,
        obj: "User",
        publishEvent: bool = False,
        generateNewId: bool = False,
        skipValidation: bool = False,
    ):
        logger.debug(f"[{User.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(
            id=id,
            email=obj.email(),
            password=obj.password(),
            publishEvent=publishEvent,
            skipValidation=skipValidation,
        )

    def _validateEmail(self, email):
        regex = r"^[a-zA-Z0-9]+[a-zA-Z0-9\._]+[@]\w+[.]\w{2,30}$"
        if not (re.search(regex, email)):
            raise InvalidValueException(f"Email is not valid: {email}")

    def email(self) -> str:
        return self._email

    def hasOneTimePassword(self) -> bool:
        return self.isPasswordOneTimePassword()

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if (
            "email" in data
            and data["email"] != self._email
            and data["email"] is not None
        ):
            updated = True
            self._email = data["name"]
        if (
            "password" in data
            and data["password"] != self._password
            and data["password"] is not None
        ):
            updated = True
            self._password = data["password"]
        if updated:
            self.publishUpdate(old)

    def setPassword(self, password: str):
        from src.domain_model.user.UserPasswordSet import UserPasswordSet

        self._password = password
        DomainPublishedEvents.addEventForPublishing(UserPasswordSet(self))

    def password(self) -> str:
        return self._password

    def generateOneTimePassword(self):
        from src.domain_model.user.UserOneTimePasswordGenerated import (
            UserOneTimePasswordGenerated,
        )

        self._password = f'{str(uuid4()).replace("-", "")}{User.ONE_TIME_PASSWORD_TAG}'
        DomainPublishedEvents.addEventForPublishing(UserOneTimePasswordGenerated(self))

    def isPasswordOneTimePassword(self) -> bool:
        return self._password.endswith(User.ONE_TIME_PASSWORD_TAG)

    def stripOneTimePasswordTag(self):
        return self._password.replace(User.ONE_TIME_PASSWORD_TAG, "")

    def publishDelete(self):
        from src.domain_model.user.UserDeleted import UserDeleted

        DomainPublishedEvents.addEventForPublishing(UserDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user.UserUpdated import UserUpdated

        DomainPublishedEvents.addEventForPublishing(UserUpdated(old, self))

    def toMap(self) -> dict:
        return {"user_id": self.id(), "email": self.email()}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, User):
            raise NotImplementedError(
                f"other: {other} can not be compared with User class"
            )
        return (
            self.id() == other.id()
            and self.email() == other.email()
            and self.password() == other.password()
        )


