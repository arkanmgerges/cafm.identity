"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from abc import ABC
from uuid import uuid4

from src.resource.common.DateTimeHelper import DateTimeHelper


class DomainEvent(ABC):
    def __init__(self, id: str = str(uuid4()), name: str = "", occurredOn: int = None, key: str = None):
        self._id = id
        self._key = key
        self._name = name
        self._occurredOn = DateTimeHelper.utcNow() if occurredOn is None else occurredOn
        self._data = {}

    def key(self) -> str:
        """Get the key of the event, a lot of events can have the same key but different id,
        the key is used as a grouping mechanism

        Returns:
            str: The key of the event
        """
        return self._key

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
        """When the event happened"""
        return self._occurredOn

    def data(self) -> dict:
        """Get data associated for this object (assigned by the derived classes)

        Returns:
            dict: Data of the event
        """
        return self._data
