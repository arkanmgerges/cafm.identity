"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.realm.Realm import Realm
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User


class UserIncludesRealmsAndRoles(HasToMap):
    def __init__(self, user: User, realms: List[Realm] = None, roles: List[Role] = None):
        self._realms = realms if realms is not None else []
        self._roles = roles if roles is not None else []
        self._user = user

    @classmethod
    def createFrom(cls, user: User, realms: List[Realm] = None, roles: List[Role] = None, **_kwargs):
        return UserIncludesRealmsAndRoles(user=user, realms=realms, roles=roles)

    def id(self) -> str:
        return self._user.id()

    def email(self) -> str:
        return self._user.email()

    def realms(self) -> List[Realm]:
        return self._realms

    def roles(self) -> List[Role]:
        return self._roles

    def toMap(self) -> dict:
        return {**self._user.toMap(), **{"realms": [x.toMap() for x in self._realms], "roles": [x.toMap() for x in self._roles]}}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

