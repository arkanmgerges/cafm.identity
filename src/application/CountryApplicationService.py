"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.country.CountryRepository import CountryRepository
from src.resource.logging.decorator import debugLogger
from src.domain_model.country.Country import Country


class CountryApplicationService:
    def __init__(
        self, countryRepository: CountryRepository, authzService: AuthorizationService
    ):
        self._countryRepository = countryRepository
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def countries(
        self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None
    ) -> dict:
        return self._countryRepository.countries(
            resultFrom=resultFrom, resultSize=resultSize, order=order
        )

    @debugLogger
    def countryById(self, id: int) -> Country:
        resource = self._countryRepository.countryById(id=id)
        return resource

    @debugLogger
    def citiesByCountryId(
        self,
        id: int,
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        return self._countryRepository.citiesByCountryId(
            id=id, resultFrom=resultFrom, resultSize=resultSize, order=order
        )

    @debugLogger
    def cityByCountryId(self, countryId: int, cityId: int):
        return self._countryRepository.cityByCountryId(
            countryId=countryId, cityId=cityId
        )

    @debugLogger
    def statesByCountryId(
        self,
        id: int,
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        return self._countryRepository.statesByCountryId(
            id=id, resultFrom=resultFrom, resultSize=resultSize, order=order
        )

    @debugLogger
    def citiesByCountryIdAndStateId(
        self,
        countryId: int = 0,
        stateId: str = "",
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        return self._countryRepository.citiesByCountryIdAndStateId(
            countryId=countryId, stateId=stateId, resultFrom=resultFrom, resultSize=resultSize, order=order
        )
