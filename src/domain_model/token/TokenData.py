"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List


class TokenData:
    def __init__(self, id: str, email: str, roles: List[dict]):
        self._id = id
        self._email = email
        self._roles = roles

    def id(self) -> str:
        return self._id

    def email(self) -> str:
        return self._email

    def roles(self) -> List[dict]:
        return self._roles

    def toMap(self) -> dict:
        return {"id": self.id(), "email": self.email(), "roles": str(self.roles())}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, TokenData):
            raise NotImplementedError(
                f"other: {other} can not be compared with TokenData class"
            )
        return self.id() == other.id() and self.email() == other.email()
