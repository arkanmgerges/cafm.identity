"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.common.HasToMap import HasToMap


class Resource(HasToMap):
    def __init__(self, id: str = None, type: str = ""):
        self._id = str(uuid4()) if id is None else id
        self._type = type

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return self._type

    def toMap(self) -> dict:
        return {"resource_id": self.id(), "type": self.type()}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"
