"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

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

    @abstractmethod
    def userById(self, id: str) -> User:
        """Get user by id

        Args:
            id (str): The id of the user

        Returns:
            User: user object
        """

    @abstractmethod
    def usersByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[User]:
        """Get list of users based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[User]: A list of users
        """

    @abstractmethod
    def deleteUser(self, user: User) -> None:
        """Delete a user

        Args:
            user (User): The user that needs to be deleted
        """

    @abstractmethod
    def updateUser(self, user: User) -> None:
        """Update a user

        Args:
            user (User): The user that needs to be updated
        """