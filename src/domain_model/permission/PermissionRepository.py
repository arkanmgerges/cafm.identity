"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.permission.Permission import Permission


class PermissionRepository(ABC):
    @abstractmethod
    def createPermission(self, permission: Permission):
        """Create permission

        Args:
            permission (Permission): The permission that needs to be created

        """

    @abstractmethod
    def permissionByName(self, name: str) -> Permission:
        """Get permission by name

        Args:
            name (str): The name of the permission

        Returns:
            Permission: permission object
        """

    @abstractmethod
    def permissionById(self, id: str) -> Permission:
        """Get permission by id

        Args:
            id (str): The id of the permission

        Returns:
            Permission: permission object
        """

    @abstractmethod
    def permissionsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                order: List[dict] = None) -> dict:
        """Get list of permissions based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def deletePermission(self, permission: Permission) -> None:
        """Delete a permission

        Args:
            permission (Permission): The permission that needs to be deleted
        """

    @abstractmethod
    def updatePermission(self, permission: Permission) -> None:
        """Update a permission

        Args:
            permission (Permission): The permission that needs to be updated
        """
