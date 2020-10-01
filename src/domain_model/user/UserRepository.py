"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.user.User import User


class UserRepository(ABC):
    @abstractmethod
    def createUser(self, user: User):
        """Create user

        Args:
            user (User): The user that needs to be created

        """

    @abstractmethod
    def userByName(self, name: str) -> User:
        """Get user by name

        Args:
            name (str): The name of the user

        Returns:
            User: user object
        """

    @abstractmethod
    def userByNameAndPassword(self, name: str, password: str) -> User:
        """Get user by name and password

        Args:
            name (str): The name of the user
            password (str): The password of the user

        Returns:
            User: user object
        """
