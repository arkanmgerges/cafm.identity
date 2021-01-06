"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.CountryApplicationService import CountryApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.domain_model.resource.exception.CountryDoesNotExistException import CountryDoesNotExistException
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.domain_model.country.Country import Country
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.country_app_service_pb2 import CountryAppService_countriesResponse, \
    CountryAppService_countryByIdResponse
from src.resource.proto._generated.identity.country_app_service_pb2_grpc import CountryAppServiceServicer


class CountryAppServiceListener(CountryAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def countries(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{CountryAppServiceListener.countries.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = countryAppService.countries(
                resultFrom=request.resultFrom,
                resultSize=resultSize,
                token=token,
                order=orderData)
            response = CountryAppService_countriesResponse()
            for country in result['items']:
                response.countries.add(id=country.id(), geoNameId=country.geoNameId(), localeCode=country.localeCode(),
                                       continentCode=country.continentCode(), continentName=country.continentName(),
                                       countryIsoCode=country.countryIsoCode(), countryName=country.countryName(),
                                       isInEuropeanUnion=country.isInEuropeanUnion())
            response.itemCount = result['itemCount']
            logger.debug(f'[{CountryApplicationService.countries.__qualname__}] - response: {response}')
            return CountryAppService_countriesResponse(countries=response.countries, itemCount=response.itemCount)
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countriesResponse()

    @debugLogger
    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''

    def countryById(self, request, context):
        try:
            token = self._token(context)
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)
            country: Country = countryAppService.countryById(id=request.id, token=token)
            logger.debug(f'[{CountryAppServiceListener.countryById.__qualname__}] - response: {country}')
            response = CountryAppService_countryByIdResponse()
            response.country.id = country.id()
            response.country.geoNameId = country.geoNameId()
            response.country.localeCode = country.localeCode()
            response.country.continentCode = country.continentCode()
            response.country.continentName = country.continentName()
            response.country.countryIsoCode = country.countryIsoCode()
            response.country.countryName = country.countryName()
            response.country.isInEuropeanUnion = country.isInEuropeanUnion()
            return response
        except CountryDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('country does not exist')
            return CountryAppService_countryByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countryByIdResponse()
