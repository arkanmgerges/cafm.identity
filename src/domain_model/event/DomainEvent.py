"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from abc import ABC
from uuid import uuid4


class DomainEvent(ABC):
    def __init__(self, id: str = str(uuid4()), name: str = '', occurredOn: int = round(time.time() * 1000)):
        self._id = id
        self._name = name
        self._occurredOn = occurredOn
        self._data = {}

    def id(self) -> str:
        """Get identity of the object

        Returns:
             str: Identity of the object
        """
        return self._id

    def name(self) -> str:
        """Get the name of the event

        Returns:
            str: The name of the event
        """
        return self._name

    def occurredOn(self) -> int:
        """When the event happened

        """
        return self._occurredOn

    def data(self) -> dict:
        """Get data associated for this object (assigned by the derived classes)

        Returns:
            dict: Data of the event
        """
        return self._data
