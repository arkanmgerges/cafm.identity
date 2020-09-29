"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

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