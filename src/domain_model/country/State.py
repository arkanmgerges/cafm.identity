"""
    @author: Mohammad S. moso<moso@develoop.run>
"""

from src.domain_model.resource.Resource import Resource
from src.resource.logging.logger import logger


class State(Resource):
    def __init__(self, id: str, name: str = ''):
        super().__init__(id=id, type='state')

        self._name = name

    @classmethod
    def createFrom(self, id: str, name: str = ''):
        logger.debug(f'[{State.createFrom.__qualname__}] - with id {id}')

        state = State(id=id, name=name)
        return state

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, State):
            raise NotImplementedError(f'other: {other} can not be compared with State class')
        return self.id() == other.id() and self.name() == other.name()
