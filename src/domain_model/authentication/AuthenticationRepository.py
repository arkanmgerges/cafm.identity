"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod


class AuthenticationRepository(ABC):
    @abstractmethod
    def authenticateUserByEmailAndPassword(self, email: str, password: str) -> dict:
        """Authenticate user and return dict for id, role, and name

        Args:
            email (str): email of the user to be authenticated
            password (str): user password used for authentication

        Returns:
            dict: Authentication dictionary, e.g. {'id': 1234, 'role': ['r1', 'r2', ...], 'name': 'john'}

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """

    @abstractmethod
    def persistToken(self, token: str, ttl: int = 300) -> None:
        """Save the token for a period of time measured in seconds

        Args:
            token (str): The token to be persisted
            ttl (int): time to live measured in seconds, if the ttl is -1 then the token will be persisted forever
        """

    @abstractmethod
    def refreshToken(self, token: str, ttl: int = 300) -> None:
        """Refresh the ttl of the token

        Args:
            token (str): The token to be refreshed
            ttl (int): time to live measured in seconds, if the ttl is -1 then the token will be persisted forever
        """

    @abstractmethod
    def tokenExists(self, token: str) -> bool:
        """Check if the token does exist

        Args:
            token (str): The token to be checked

        Returns:
            bool: If True then the token exists, False if it does not exist
        """

    @abstractmethod
    def deleteToken(self, token: str) -> None:
        """Delete the token

        Args:
            token (str): The token to be deleted
        """
