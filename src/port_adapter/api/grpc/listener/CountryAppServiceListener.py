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
    CountryAppService_countryByIdResponse, CountryAppService_countryCitiesResponse
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
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            logger.debug(
                f'[{CountryAppServiceListener.countries.__qualname__}] - metadata: {metadata}\n\t resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = countryAppService.countries(
                resultFrom=request.resultFrom,
                resultSize=resultSize,
                order=orderData)
            response = CountryAppService_countriesResponse()
            response.itemCount = result['itemCount']
            for country in result['items']:
                response.countries.add(id=country.id(), geoNameId=country.geoNameId(), localeCode=country.localeCode(),
                                       continentCode=country.continentCode(), continentName=country.continentName(),
                                       countryIsoCode=country.countryIsoCode(), countryName=country.countryName(),
                                       isInEuropeanUnion=country.isInEuropeanUnion())
            logger.debug(f'[{CountryApplicationService.countries.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countriesResponse()

    def countryById(self, request, context):
        try:
            metadata = context.invocation_metadata()
            logger.debug(
                f'[{CountryAppServiceListener.countryById.__qualname__}] - metadata: {metadata}\n\t id: {request.id}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            country: Country = countryAppService.countryById(id=request.id)
            response = CountryAppService_countryByIdResponse()
            response.country.id = country.id()
            response.country.geoNameId = country.geoNameId()
            response.country.localeCode = country.localeCode()
            response.country.continentCode = country.continentCode()
            response.country.continentName = country.continentName()
            response.country.countryIsoCode = country.countryIsoCode()
            response.country.countryName = country.countryName()
            response.country.isInEuropeanUnion = country.isInEuropeanUnion()
            logger.debug(f'[{CountryApplicationService.countryById.__qualname__}] - response: {response}')
            return response
        except CountryDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('country does not exist')
            return CountryAppService_countryByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countryByIdResponse()

    def countryCities(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            logger.debug(
                f'[{CountryAppServiceListener.countryCities.__qualname__}] - metadata: {metadata}\n\t \ '
                f'id: {request.id},resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = countryAppService.countryCities(id=request.id, resultFrom=request.resultFrom,
                                                           resultSize=resultSize, order=orderData)
            response = CountryAppService_countryCitiesResponse()
            response.itemCount = result['itemCount']
            for city in result['items']:
                response.cities.add(id=city.id(), geoNameId=city.geoNameId(), localeCode=city.localeCode(),
                                    continentCode=city.continentCode(), continentName=city.continentName(),
                                    countryIsoCode=city.countryIsoCode(), countryName=city.countryName(),
                                    subdivisionOneIsoCode=city.subdivisionOneIsoCode(),
                                    subdivisionOneIsoName=city.subdivisionOneIsoName(),
                                    subdivisionTwoIsoCode=city.subdivisionTwoIsoCode(),
                                    subdivisionTwoIsoName=city.subdivisionTwoIsoName(), cityName=city.cityName(),
                                    metroCode=city.metroCode(), timeZone=city.timeZone(),
                                    isInEuropeanUnion=city.isInEuropeanUnion())
            logger.debug(f'[{CountryApplicationService.countryCities.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countryCitiesResponse()
