"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def canHandle(self, name: str) -> bool:
        """Can handle the command

        Args:
            name (str): The command name

        Returns:
            bool: Returns True if it can handle the command, False otherwise
        """

    @abstractmethod
    def handleCommand(self, name: str, data: dict) -> dict:
        """Handle the command

        Args:
            name (str): Command name to handle
            data (dict): The associated data for the command to handle

        Returns:
            dict: The result of the handler
        """