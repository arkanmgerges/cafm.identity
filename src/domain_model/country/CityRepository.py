"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.country.City import City


class CityRepository(ABC):
    @abstractmethod
    def cities(
        self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None
    ) -> dict:
        """Get list of cities

        Args:
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "totalItemCount": 0}
        """

    @abstractmethod
    def cityById(self, id: str) -> City:
        """Get city by id

        Args:
            id (str): The id of the city

        Returns:
            User: user object

        :raises:
            `CountryDoesNotExistException <src.domain_model.resource.exception.CountryDoesNotExistException>` Raise an exception if the city does not exist
        """
