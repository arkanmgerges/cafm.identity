"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.policy.model.UserIncludesRoles import UserIncludesRoles
from src.domain_model.realm.Realm import Realm


class RealmIncludesUsersIncludeRoles(HasToMap):
    def __init__(self, realm: Realm, usersIncludeRoles: List[UserIncludesRoles]):
        self._realm = realm
        self._usersIncludeRoles = usersIncludeRoles if usersIncludeRoles is not None else []

    @classmethod
    def createFrom(cls, realm: Realm, usersIncludeRoles: List[UserIncludesRoles], **_kwargs):
        return RealmIncludesUsersIncludeRoles(realm=realm, usersIncludeRoles=usersIncludeRoles)

    def id(self) -> str:
        return self._realm.id()

    def name(self) -> str:
        return self._realm.name()

    def realmType(self) -> str:
        return self._realm.realmType()

    def usersIncludeRoles(self) -> List[UserIncludesRoles]:
        return self._usersIncludeRoles

    def toMap(self) -> dict:
        return {**self._realm.toMap(), **{"users_include_roles": [x.toMap() for x in self._usersIncludeRoles]}}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

