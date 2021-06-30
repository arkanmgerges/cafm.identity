"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User


class UserIncludesRoles(HasToMap):
    def __init__(self, user: User, roles: List[Role] = None):
        self._user = user
        self._roles = roles if roles is not None else []

    @classmethod
    def createFrom(cls, user: User, roles: List[Role], **_kwargs):
        return UserIncludesRoles(user=user, roles=roles)

    def id(self) -> str:
        return self._user.id()

    def email(self) -> str:
        return self._user.email()

    def roles(self) -> List[Role]:
        return self._roles

    def toMap(self) -> dict:
        return {**self._user.toMap(), **{"roles": [x.toMap() for x in self._roles]}}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

