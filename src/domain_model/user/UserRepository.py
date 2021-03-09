"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user.User import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, obj: User, tokenData: TokenData):
        """Save user

        Args:
            obj (User): The user that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deleteUser(self, obj: User, tokenData: TokenData) -> None:
        """Delete a user

        Args:
            obj (User): The user that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the user could not be deleted            
        """

    @abstractmethod
    def deleteUserOneTimePassword(self, obj: User, tokenData: TokenData) -> None:
        """Delete a user one time password

        Args:
            obj (User): The user that needs for its one time password to be deleted
            tokenData (TokenData): Token data used for deleting the resource
        """

    @abstractmethod
    def setUserPassword(self, obj: User, tokenData: TokenData) -> None:
        """Set a user password

        Args:
            obj (User): The user that needs for its one time password to be deleted
            tokenData (TokenData): Token data used for deleting the resource
        """

    @abstractmethod
    def userByEmail(self, email: str) -> User:
        """Get user by name

        Args:
            email (str): The email of the user

        Returns:
            User: user object
            
        :raises:
            `UserDoesNotExistException <src.domain_model.resource.exception.UserDoesNotExistException>` Raise an exception if the user does not exist            
        """

    @abstractmethod
    def userByEmailAndPassword(self, email: str, password: str) -> User:
        """Get user by name and password

        Args:
            email (str): The email of the user
            password (str): The password of the user

        Returns:
            User: user object
            
        :raises:
            `UserDoesNotExistException <src.domain_model.resource.exception.UserDoesNotExistException>` Raise an exception if the user does not exist            
        """

    @abstractmethod
    def userById(self, id: str) -> User:
        """Get user by id

        Args:
            id (str): The id of the user

        Returns:
            User: user object
            
        :raises:
            `UserDoesNotExistException <src.domain_model.resource.exception.UserDoesNotExistException>` Raise an exception if the user does not exist
        """

    @abstractmethod
    def users(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData], resultFrom: int = 0,
              resultSize: int = 100,
              order: List[dict] = None) -> dict:
        """Get list of users based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """
