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
    def permissionsByOwnedPermissions(self, ownedPermissions: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Permission]:
        """Get list of permissions based on the owned permissions that the user has

        Args:
            ownedPermissions (List[str]): A list of the permissions that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[Permission]: A list of permissions
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