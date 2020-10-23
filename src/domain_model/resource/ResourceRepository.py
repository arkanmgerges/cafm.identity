"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.resource.Resource import Resource


class ResourceRepository(ABC):
    @abstractmethod
    def resourceById(self, id: str = '') -> Resource:
        """Retrieve a resource by id

        Args:
            id (str): Resource id that is used to fetch the resource

        Returns:
            Resource: The resource to be fetched
        """
