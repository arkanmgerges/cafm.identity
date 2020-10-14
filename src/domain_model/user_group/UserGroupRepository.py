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
    def userGroupsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                               order: List[dict] = None) -> dict:
        """Get list of userGroups based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
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
