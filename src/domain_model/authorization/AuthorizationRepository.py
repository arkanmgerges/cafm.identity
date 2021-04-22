"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List


class AuthorizationRepository(ABC):
    @abstractmethod
    def rolesByUserId(self, id: str) -> List[str]:
        """Get roles by user id

        Args:
            id (str): id of the user

        Returns:
            List[str]: List of roles

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """

    @abstractmethod
    def tokenExists(self, token: str) -> bool:
        """Check if the token does exist

        Args:
            token (str): The token to be checked

        Returns:
            bool: If True then the token exists, False if it does not exist
        """
