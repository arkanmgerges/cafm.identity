"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData
from src.domain_model.country.Country import Country


class CountryRepository(ABC):

    @abstractmethod
    def countries(self, resultFrom: int = 0,
                  resultSize: int = 100,
                  order: List[dict] = None) -> dict:
        """Get list of users based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def countryById(self, id: str) -> Country:
        """Get user by id

        Args:
            id (str): The id of the user

        Returns:
            User: user object

        :raises:
            `UserDoesNotExistException <src.domain_model.resource.exception.UserDoesNotExistException>` Raise an exception if the user does not exist
        """

    @abstractmethod
    def countryCities(self, id: str = '',
                      resultFrom: int = 0,
                      resultSize: int = 100,
                      order: List[dict] = None) -> dict:
        """Get user by id

        Args:
            id (str): The id of the user

        Returns:
            User: user object

        :raises:
            `UserDoesNotExistException <src.domain_model.resource.exception.UserDoesNotExistException>` Raise an exception if the user does not exist
        """
