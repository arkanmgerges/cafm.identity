"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData


class PermissionRepository(ABC):
    @abstractmethod
    def save(self, obj: Permission, tokenData: TokenData):
        """Save permission

        Args:
            obj (Permission): The permission that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def createPermission(self, obj: Permission, tokenData: TokenData):
        """Create permission

        Args:
            obj (Permission): The permission that needs to be created
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deletePermission(self, obj: Permission, tokenData: TokenData) -> None:
        """Delete a permission

        Args:
            obj (Permission): The permission that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the permission could not be deleted            
        """

    @abstractmethod
    def updatePermission(self, obj: Permission, tokenData: TokenData) -> None:
        """Update a permission

        Args:
            obj (Permission): The permission that needs to be updated
            tokenData (TokenData): Token data used for updating the resource

        :raises:
            `ObjectCouldNotBeUpdatedException <src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException>` Raise an exception if the permission could not be updated
        """

    @abstractmethod
    def permissionByName(self, name: str) -> Permission:
        """Get permission by name

        Args:
            name (str): The name of the permission

        Returns:
            Permission: permission object

        :raises:
            `PermissionDoesNotExistException <src.domain_model.resource.exception.PermissionDoesNotExistException>` Raise an exception if the permission does not exist            
        """

    @abstractmethod
    def permissionById(self, id: str) -> Permission:
        """Get permission by id

        Args:
            id (str): The id of the permission

        Returns:
            Permission: permission object
            
        :raises:
            `PermissionDoesNotExistException <src.domain_model.resource.exception.PermissionDoesNotExistException>` Raise an exception if the permission does not exist
        """

    @abstractmethod
    def permissions(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData],
                    resultFrom: int = 0, resultSize: int = 100,
                    order: List[dict] = None) -> dict:
        """Get list of permissions based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """
