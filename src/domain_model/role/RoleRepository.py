"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.role.Role import Role


class RoleRepository(ABC):
    @abstractmethod
    def createRole(self, role: Role):
        """Create role

        Args:
            role (Role): The role that needs to be created

        """

    @abstractmethod
    def roleByName(self, name: str) -> Role:
        """Get role by name

        Args:
            name (str): The name of the role

        Returns:
            Role: role object
        """