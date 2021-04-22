"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from abc import ABC, abstractmethod
from typing import Any, List


class Consumer(ABC):
    """Message consumer from the message broker"""

    @abstractmethod
    def poll(self, timeout: float = None) -> Any:
        """Send message to the message broker

        Args:
            timeout (float): Maximum time (seconds) to block waiting for message, event or callback

        """
        pass

    @abstractmethod
    def commit(self):
        """Commit the offset of the consumer"""
        pass

    @abstractmethod
    def close(self):
        """Commit the final offsets (if auto commit is enabled) and close the connection"""
        pass

    @abstractmethod
    def position(self, partitions: List[Any]) -> List[Any]:
        """Retrieve current positions (offsets) for the list of partitions

        Args:
            partitions (List[Any]): List of topic+partitions to return current offsets for. The current offset is the
            offset of the last consumed message + 1
        """
        pass

    @abstractmethod
    def consumerGroupMetadata(self) -> Any:
        """Consumer's current group metadata"""
        pass

    @abstractmethod
    def assignment(self) -> List[Any]:
        """Returns the current partition assignment"""
        pass

    @abstractmethod
    def subscribe(self, topics: List[str]) -> None:
        """Set subscription to supplied list of topics This replaces a previous subscription.
        Regexp pattern subscriptions are supported by prefixing the topic string with "^"

        """
        pass

    @abstractmethod
    def unsubscribe(self) -> None:
        """Remove current subscription"""
        pass
