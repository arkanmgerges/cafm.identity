"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user_group.UserGroup import UserGroup


class UserGroupRepository(ABC):
    @abstractmethod
    def save(self, obj: UserGroup, tokenData: TokenData):
        """Save user group

        Args:
            obj (UserGroup): The user group that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deleteUserGroup(self, obj: UserGroup, tokenData: TokenData) -> None:
        """Delete a user group

        Args:
            obj (UserGroup): The user group that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the user group could not be deleted
        """

    @abstractmethod
    def userGroupByName(self, name: str) -> UserGroup:
        """Get userGroup by name

        Args:
            name (str): The name of the userGroup

        Returns:
            UserGroup: userGroup object
            
        :raises:
            `UserGroupDoesNotExistException <src.domain_model.resource.exception.UserGroupDoesNotExistException>` Raise an exception if the user group does not exist            
        """

    @abstractmethod
    def userGroupById(self, id: str) -> UserGroup:
        """Get userGroup by id

        Args:
            id (str): The id of the userGroup

        Returns:
            UserGroup: userGroup object
            
        :raises:
            `UserGroupDoesNotExistException <src.domain_model.resource.exception.UserGroupDoesNotExistException>` Raise an exception if the user group does not exist            
        """

    @abstractmethod
    def userGroups(self, tokenData: TokenData, roleAccessPermissionData:List[RoleAccessPermissionData], resultFrom: int = 0, resultSize: int = 100,
                        order: List[dict] = None) -> dict:
        """Get list of userGroups based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """
