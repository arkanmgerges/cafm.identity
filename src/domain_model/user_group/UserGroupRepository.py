"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.user_group.UserGroup import UserGroup


class UserGroupRepository(ABC):
    @abstractmethod
    def createUserGroup(self, userGroup: UserGroup):
        """Create userGroup

        Args:
            userGroup (UserGroup): The userGroup that needs to be created

        """

    @abstractmethod
    def userGroupByName(self, name: str) -> UserGroup:
        """Get userGroup by name

        Args:
            name (str): The name of the userGroup

        Returns:
            UserGroup: userGroup object
        """
        
    @abstractmethod
    def userGroupById(self, id: str) -> UserGroup:
        """Get userGroup by id

        Args:
            id (str): The id of the userGroup

        Returns:
            UserGroup: userGroup object
        """

    @abstractmethod
    def userGroupsByOwnedUserGroups(self, ownedUserGroups: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[UserGroup]:
        """Get list of userGroups based on the owned userGroups that the user has

        Args:
            ownedUserGroups (List[str]): A list of the userGroups that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[UserGroup]: A list of userGroups
        """
        
    @abstractmethod
    def deleteUserGroup(self, userGroup: UserGroup) -> None:
        """Delete a userGroup

        Args:
            userGroup (UserGroup): The userGroup that needs to be deleted
        """

    @abstractmethod
    def updateUserGroup(self, userGroup: UserGroup) -> None:
        """Update a userGroup

        Args:
            userGroup (UserGroup): The userGroup that needs to be updated
        """