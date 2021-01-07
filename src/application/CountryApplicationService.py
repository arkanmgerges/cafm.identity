"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.country.CountryRepository import CountryRepository
from src.resource.logging.decorator import debugLogger
from src.domain_model.country.Country import Country


class CountryApplicationService:
    def __init__(self, countryRepository: CountryRepository, authzService: AuthorizationService):
        self._countryRepository = countryRepository
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def countries(self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        return self._countryRepository.countries(resultFrom=resultFrom, resultSize=resultSize, order=order)

    @debugLogger
    def countryById(self, id: str) -> Country:
        resource = self._countryRepository.countryById(id=id)
        return resource

    def countryCities(self, id: str, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        return self._countryRepository.countryCities(id=id, resultFrom=resultFrom, resultSize=resultSize, order=order)
