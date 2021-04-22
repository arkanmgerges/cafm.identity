"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User


class HelperRepository(ABC):
    @abstractmethod
    def roleDocumentId(self, id: str) -> str:
        """Retrieve role document id

        Args:
            id (str): Role id to retrieve its document id

        Returns:
            str: Document id
        """

    @abstractmethod
    def userDocumentId(self, id: str) -> str:
        """Retrieve user document id

        Args:
            id (str): User id to retrieve its document id

        Returns:
            str: Document id
        """

    @abstractmethod
    def resourceDocumentId(self, resource: Resource) -> str:
        """Retrieve doc id for a resource

        Args:
            resource (Resource): A resource to retrieve its document id

        Returns:
            str: Document id
        """
