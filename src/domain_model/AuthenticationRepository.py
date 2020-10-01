"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod


class AuthenticationRepository(ABC):
    @abstractmethod
    def authenticateUserByNameAndPassword(self, name: str, password: str) -> dict:
        """Authenticate user and return dict for id, role, and name

        Args:
            name (str): name of user to be authenticated
            password (str): user password used for authentication

        Returns:
            dict: Authentication dictionary, e.g. {'id': 1234, 'role': ['r1', 'r2', ...], 'name': 'john'}

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """

