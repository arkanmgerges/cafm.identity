"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.country.City import City
from src.domain_model.country.Country import Country


class CountryRepository(ABC):

    @abstractmethod
    def countries(self, resultFrom: int = 0,
                  resultSize: int = 100,
                  order: List[dict] = None) -> dict:
        """Get list of countries

        Args:
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def countryById(self, id: int = 0) -> Country:
        """Get country by id

        Args:
            id (str): The id of the country

        Returns:
            Country: country object

        :raises:
            `CountryDoesNotExistException <src.domain_model.resource.exception.CountryDoesNotExistException>` Raise an exception if the country does not exist
        """

    @abstractmethod
    def citiesByCountryId(self, id: int = 0,
                          resultFrom: int = 0,
                          resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        """Get a country cities by country id

        Args:
            id (int): The id of the country
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def cityByCountryId(self, countryId: int = 0, cityId: int = 0) -> City:
        """Get city by country id and city id

        Args:
            countryId (int): The id of the country
            cityId (str): The id of the city

        Returns:
            City: city object

        :raises:
            `CountryDoesNotExistException <src.domain_model.resource.exception.CountryDoesNotExistException>` Raise an exception if the city does not exist
        """
