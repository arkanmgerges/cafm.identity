"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domainmodel.permission.Permission import Permission


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