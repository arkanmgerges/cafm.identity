"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domainmodel.user.User import User


class UserRepository(ABC):
    @abstractmethod
    def createUser(self, user: User):
        """Create user

        Args:
            user (User): The user that needs to be created

        """

    @abstractmethod
    def userByUsername(self, username: str) -> User:
        """Get user by username
        Args:
            username (str): The username of the user
        Returns:
            User: user object
        """
