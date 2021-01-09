"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class MessageBase(ABC, object):
    @abstractmethod
    def topic(self):
        """Retrieve the topic that this message will use

        Returns:
              str: Topic that this message is using
        """
        pass

    @abstractmethod
    def toMap(self, *args):
        """Retrieve object dictionary
        Args:
            *args: Arguments associated for calling this method

        Returns:
            dict: Dictionary data of the object
        """
        pass

    @abstractmethod
    def msgId(self) -> str:
        """Retrieve message id

        """
        pass

    @abstractmethod
    def msgKey(self) -> str:
        """Retrieve message key

        """
