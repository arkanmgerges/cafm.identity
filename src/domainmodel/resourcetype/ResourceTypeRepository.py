"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domainmodel.resourcetype.ResourceType import ResourceType


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