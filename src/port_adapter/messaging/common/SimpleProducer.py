"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from abc import ABC, abstractmethod

from src.port_adapter.messaging.common.model.MessageBase import MessageBase


class SimpleProducer(ABC):
    """Message producer to the message broker"""

    @abstractmethod
    def produce(self, obj: MessageBase, schema: dict) -> None:
        """Send message to the message broker

        Args:
            obj (MessageBase): The object model that is needed to be sent
            schema (dict): The schema that will be used for data validation

        """
        pass
