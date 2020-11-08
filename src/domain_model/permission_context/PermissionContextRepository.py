"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.permission_context.PermissionContext import PermissionContext


class PermissionContextRepository(ABC):
    @abstractmethod
    def createPermissionContext(self, permissionContext: PermissionContext):
        """Create permissionContext

        Args:
            permissionContext (PermissionContext): The permissionContext that needs to be created
        """

    @abstractmethod
    def permissionContextByName(self, name: str) -> PermissionContext:
        """Get permissionContext by name

        Args:
            name (str): The name of the permissionContext

        Returns:
            PermissionContext: permissionContext object
            
        :raises:
            `PermissionContextDoesNotExistException <src.domain_model.resource.exception.PermissionContextDoesNotExistException>` Raise an exception if the permission context does not exist
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
    def permissionContextsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                                  order: List[dict] = None) -> dict:
        """Get list of permissionContexts based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def deletePermissionContext(self, permissionContext: PermissionContext) -> None:
        """Delete a permissionContext

        Args:
            permissionContext (PermissionContext): The permissionContext that needs to be deleted
            
        :raises:        
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the permission context could not be deleted
        """

    @abstractmethod
    def updatePermissionContext(self, permissionContext: PermissionContext) -> None:
        """Update a permissionContext

        Args:
            permissionContext (PermissionContext): The permissionContext that needs to be updated
            
        :raises:
            `ObjectCouldNotBeUpdatedException <src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException>` Raise an exception if the permission context could not be updated
        """
