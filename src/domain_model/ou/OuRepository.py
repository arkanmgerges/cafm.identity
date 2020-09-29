"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.ou.Ou import Ou


class OuRepository(ABC):
    @abstractmethod
    def createOu(self, ou: Ou):
        """Create ou

        Args:
            ou (Ou): The ou that needs to be created

        """

    @abstractmethod
    def ouByName(self, name: str) -> Ou:
        """Get ou by name

        Args:
            name (str): The name of the ou

        Returns:
            Ou: ou object
        """