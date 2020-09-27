"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from abc import ABC, abstractmethod
from uuid import uuid4


class DomainEvent(ABC):
    def __init__(self, id: str = str(uuid4()), occurredOn: int = time.time() * 1000):
        self._id = id
        self._occurredOn = occurredOn
        self._data = ''

    def id(self) -> str:
        """Get identity of the object

        Returns (str): Identity of the object
        """
        return self._id

    def occurredOn(self) -> int:
        """When the event happened

        """
        return self._occurredOn

    def data(self) -> str:
        """Get data associated for this object (assigned by the derived classes)

        Returns (str): Data of the event
        """
        return self._data
