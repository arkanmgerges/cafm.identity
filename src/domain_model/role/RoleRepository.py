"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.role.Role import Role


class RoleRepository(ABC):
    @abstractmethod
    def createRole(self, role: Role):
        """Create role

        Args:
            role (Role): The role that needs to be created

        """

    @abstractmethod
    def roleByName(self, name: str) -> Role:
        """Get role by name

        Args:
            name (str): The name of the role

        Returns:
            Role: role object
        """

    @abstractmethod
    def roleById(self, id: str) -> Role:
        """Get role by id

        Args:
            id (str): The id of the role

        Returns:
            Role: role object
        """

    @abstractmethod
    def rolesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Role]:
        """Get list of roles based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[Role]: A list of roles
        """
