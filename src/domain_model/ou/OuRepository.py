"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.ou.Ou import Ou
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData


class OuRepository(ABC):
    @abstractmethod
    def save(self, obj: Ou, tokenData: TokenData):
        """Save ou

        Args:
            obj (Ou): The ou that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deleteOu(self, obj: Ou, tokenData: TokenData) -> None:
        """Delete a ou

        Args:
            obj (Ou): The ou that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the ou could not be deleted
        """

    @abstractmethod
    def ouByName(self, name: str) -> Ou:
        """Get ou by name

        Args:
            name (str): The name of the ou

        Returns:
            Ou: ou object

        :raises:
            `OuDoesNotExistException <src.domain_model.resource.exception.OuDoesNotExistException>` Raise an exception if the ou does not exist
        """

    @abstractmethod
    def ouById(self, id: str) -> Ou:
        """Get ou by id

        Args:
            id (str): The id of the ou

        Returns:
            Ou: ou object

        :raises:
            `OuDoesNotExistException <src.domain_model.resource.exception.OuDoesNotExistException>` Raise an exception if the ou does not exist
        """

    @abstractmethod
    def ous(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        """Get list of ous based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "totalItemCount": 0}
        """
