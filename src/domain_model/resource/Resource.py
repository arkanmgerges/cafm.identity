"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Resource:
    def __init__(self, id: str = None, type: str = ''):
        self._id = str(uuid4()) if id is None else id
        self._type = type

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return self._type