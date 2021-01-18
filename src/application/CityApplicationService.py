"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.country.City import City
from src.domain_model.country.CityRepository import CityRepository
from src.resource.logging.decorator import debugLogger


class CityApplicationService:
    def __init__(self, cityRepository: CityRepository, authzService: AuthorizationService):
        self._cityRepository = cityRepository
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def cities(self, resultFrom: int = 0, resultSize: int = 100, order: List[dict] = None) -> dict:
        return self._cityRepository.cities(resultFrom=resultFrom, resultSize=resultSize, order=order)

    @debugLogger
    def cityById(self, id: str) -> City:
        resource = self._cityRepository.cityById(id=id)
        return resource
