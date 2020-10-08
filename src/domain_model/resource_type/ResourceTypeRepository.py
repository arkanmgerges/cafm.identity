"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.resource_type.ResourceType import ResourceType


class ResourceTypeRepository(ABC):
    @abstractmethod
    def createResourceType(self, resourceType: ResourceType):
        """Create resourceType

        Args:
            resourceType (ResourceType): The resourceType that needs to be created

        """

    @abstractmethod
    def resourceTypeByName(self, name: str) -> ResourceType:
        """Get resourceType by name

        Args:
            name (str): The name of the resourceType

        Returns:
            ResourceType: resourceType object
        """
        
    @abstractmethod
    def resourceTypeById(self, id: str) -> ResourceType:
        """Get resourceType by id

        Args:
            id (str): The id of the resourceType

        Returns:
            ResourceType: resourceType object
        """

    @abstractmethod
    def resourceTypesByOwnedResourceTypes(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[ResourceType]:
        """Get list of resourceTypes based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[ResourceType]: A list of resourceTypes
        """