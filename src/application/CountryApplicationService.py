"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.country.CountryRepository import CountryRepository
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger


class CountryApplicationService:
    def __init__(self, countryRepository: CountryRepository, authzService: AuthorizationService):
        self._countryRepository = countryRepository
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def countries(self, resultFrom: int = 0, resultSize: int = 100, token: str = '',
                  order: List[dict] = None) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        return self._countryRepository.countries(tokenData=tokenData, roleAccessPermissionData=roleAccessPermissionData,
                                                 resultFrom=resultFrom,
                                                 resultSize=resultSize,
                                                 order=order)

    @debugLogger
    def countryById(self, id: str, token: str = ''):
        resource = self._countryRepository.countryById(id=id)
        # tokenData = TokenService.tokenDataFromToken(token=token)
        # roleAccessPermissionData = self._authzService.roleAccessPermissionsData(tokenData=tokenData)
        # self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessPermissionData,
        #                                 tokenData=tokenData)
        return resource
