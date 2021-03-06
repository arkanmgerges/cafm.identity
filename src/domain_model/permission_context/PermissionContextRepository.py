"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData


class PermissionContextRepository(ABC):
    @abstractmethod
    def bulkSave(self, objList: List[PermissionContext], tokenData: TokenData):
        """Bulk save permission context list

        Args:
            objList (List[PermissionContext]): The permission context list that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def bulkDelete(self, objList: List[PermissionContext], tokenData: TokenData):
        """Bulk delete permission context list

        Args:
            objList (List[PermissionContext]): The permission context list that needs to be deleted
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def save(self, obj: PermissionContext, tokenData: TokenData):
        """Save permission context

        Args:
            obj (PermissionContext): The permission context that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deletePermissionContext(
        self, obj: PermissionContext, tokenData: TokenData
    ) -> None:
        """Delete a permission context

        Args:
            obj (PermissionContext): The permission context that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the permission context could not be deleted
        """

    @abstractmethod
    def permissionContextById(self, id: str) -> PermissionContext:
        """Get permissionContext by id

        Args:
            id (str): The id of the permissionContext

        Returns:
            PermissionContext: permissionContext object

        :raises:
            `PermissionContextDoesNotExistException <src.domain_model.resource.exception.PermissionContextDoesNotExistException>` Raise an exception if the permission context does not exist
        """

    @abstractmethod
    def permissionContexts(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        """Get list of permission contexts based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "totalItemCount": 0}
        """
