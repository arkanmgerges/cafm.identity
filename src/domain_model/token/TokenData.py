"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List


class TokenData:
    def __init__(self, id: str, name: str, role: List[dict]):
        self._id = id
        self._name = name
        self._role = role

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def roles(self) -> List[dict]:
        return self._role

    def toMap(self) -> dict:
        return {'id': self.id(), 'name': self.name(),
                'role': [{'id': item['id'], 'name': item['name']} for item in self.roles()]}

    def __str__(self) -> str:
        return f'{{"id": "{self.id()}", "name": "{self.name()}", "role": {str(self.roles())}}}'

    def __eq__(self, other):
        if not isinstance(other, TokenData):
            raise NotImplementedError(f'other: {other} can not be compared with TokenData class')
        return self.id() == other.id() and self.name() == other.name()
