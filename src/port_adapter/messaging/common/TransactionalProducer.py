"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from abc import ABC, abstractmethod

from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.model.MessageBase import MessageBase


class TransactionalProducer(ABC):
    """Message producer to the message broker

    """

    @abstractmethod
    def initTransaction(self) -> None:
        """Init transaction for this producer

        """
        pass

    @abstractmethod
    def beginTransaction(self) -> None:
        """Begin transaction for this producer

        """
        pass

    @abstractmethod
    def abortTransaction(self) -> None:
        """Abort transaction for this producer

        """
        pass

    @abstractmethod
    def commitTransaction(self) -> None:
        """Begin transaction for this producer

        """
        pass

    @abstractmethod
    def produce(self, obj: MessageBase, schema: dict) -> None:
        """Send message to the message broker

        Args:
            obj (MessageBase): The object model that is needed to be sent
            schema (dict): The schema that will be used for data validation

        """
        pass

    @abstractmethod
    def sendOffsetsToTransaction(self, consumer: Consumer) -> None:
        """Commit processed message offsets to the transaction

        """
        pass
