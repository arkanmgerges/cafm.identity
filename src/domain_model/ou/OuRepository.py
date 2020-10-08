"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

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
        
    @abstractmethod
    def ouById(self, id: str) -> Ou:
        """Get ou by id

        Args:
            id (str): The id of the ou

        Returns:
            Ou: ou object
        """

    @abstractmethod
    def ousByOwnedOus(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Ou]:
        """Get list of ous based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group own
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[Ou]: A list of ous
        """