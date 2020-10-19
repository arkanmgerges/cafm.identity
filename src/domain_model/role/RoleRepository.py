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

        :raises:
            `RoleDoesNotExistException <src.domain_model.resource.exception.RoleDoesNotExistException>` Raise an exception if the role does not exist
        """

    @abstractmethod
    def roleById(self, id: str) -> Role:
        """Get role by id

        Args:
            id (str): The id of the role

        Returns:
            Role: role object

        :raises:
            `RoleDoesNotExistException <src.domain_model.resource.exception.RoleDoesNotExistException>` Raise an exception if the role does not exist
        """

    @abstractmethod
    def deleteRole(self, role: Role) -> None:
        """Delete a role

        Args:
            role (Role): The role that needs to be deleted

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the role could not be deleted
        """

    @abstractmethod
    def updateRole(self, role: Role) -> None:
        """Update a role

        Args:
            role (Role): The role that needs to be updated

        :raises:
            `ObjectCouldNotBeUpdatedException <src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException>` Raise an exception if the role could not be updated
        """

    @abstractmethod
    def rolesByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        """Get list of roles based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """
