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
from src.domain_model.country.City import City
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.country_app_service_pb2 import (CountryAppService_countriesResponse,
                                                                            CountryAppService_countryByIdResponse,
                                                                            CountryAppService_cityByCountryIdResponse,
                                                                            CountryAppService_citiesByCountryIdResponse,
                                                                            CountryAppService_statesByCountryIdResponse)
from src.resource.proto._generated.identity.country_app_service_pb2_grpc import CountryAppServiceServicer


class CountryAppServiceListener(CountryAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__countries, "Get countries", "grpc listener", "Get all countries")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def countries(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize >= 0 else 10
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
                response.countries.add(id=country.id(), localeCode=country.localeCode(),
                                       continentCode=country.continentCode(), continentName=country.continentName(),
                                       countryIsoCode=country.countryIsoCode(), countryName=country.countryName(),
                                       isInEuropeanUnion=country.isInEuropeanUnion())
            logger.debug(f'[{CountryApplicationService.countries.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_countriesResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__countryById, "Get country by id", "grpc listener", "Get a country by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def countryById(self, request, context):
        try:
            metadata = context.invocation_metadata()
            logger.debug(
                f'[{CountryAppServiceListener.countryById.__qualname__}] - metadata: {metadata}\n\t id: {request.id}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            country: Country = countryAppService.countryById(id=request.id)
            response = CountryAppService_countryByIdResponse()
            response.country.id = country.id()
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

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__citiesByCountryId, "Get cities by country id", "grpc listener", "Get cities by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def citiesByCountryId(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize >= 0 else 10
            logger.debug(
                f'[{CountryAppServiceListener.citiesByCountryId.__qualname__}] - metadata: {metadata}\n\t \ '
                f'id: {request.id},resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = countryAppService.citiesByCountryId(id=request.id, resultFrom=request.resultFrom,
                                                               resultSize=resultSize, order=orderData)
            response = CountryAppService_citiesByCountryIdResponse()
            response.itemCount = result['itemCount']
            for city in result['items']:
                response.cities.add(id=city.id(), localeCode=city.localeCode(),
                                    continentCode=city.continentCode(), continentName=city.continentName(),
                                    countryIsoCode=city.countryIsoCode(), countryName=city.countryName(),
                                    subdivisionOneIsoCode=city.subdivisionOneIsoCode(),
                                    subdivisionOneIsoName=city.subdivisionOneIsoName(), cityName=city.cityName(),
                                    timeZone=city.timeZone(), isInEuropeanUnion=city.isInEuropeanUnion())
            logger.debug(f'[{CountryApplicationService.citiesByCountryId.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_citiesByCountryIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__cityByCountryId, "Get city by country id", "grpc listener", "Get a city by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cityByCountryId(self, request, context):
        try:
            metadata = context.invocation_metadata()
            logger.debug(
                f'[{CountryAppServiceListener.cityByCountryId.__qualname__}] - metadata: {metadata}\n\t \ '
                f'country id: {request.countryId},city id: {request.cityId}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            city: City = countryAppService.cityByCountryId(countryId=request.countryId, cityId=request.cityId)

            response = CountryAppService_cityByCountryIdResponse()
            response.city.id = city.id()
            response.city.localeCode = city.localeCode()
            response.city.continentCode = city.continentCode()
            response.city.continentName = city.continentName()
            response.city.countryIsoCode = city.countryIsoCode()
            response.city.countryName = city.countryName()
            response.city.subdivisionOneIsoCode = city.subdivisionOneIsoCode()
            response.city.subdivisionOneIsoName = city.subdivisionOneIsoName()
            response.city.cityName = city.cityName()
            response.city.timeZone = city.timeZone()
            response.city.isInEuropeanUnion = city.isInEuropeanUnion()

            logger.debug(f'[{CountryApplicationService.cityByCountryId.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_cityByCountryIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__statesByCountryId, "Get states by country id", "grpc listener", "Get a states by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def statesByCountryId(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize >= 0 else 10
            logger.debug(
                f'[{CountryAppServiceListener.statesByCountryId.__qualname__}] - metadata: {metadata}\n\t \ '
                f'id: {request.id},resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            countryAppService: CountryApplicationService = AppDi.instance.get(CountryApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = countryAppService.statesByCountryId(id=request.id, resultFrom=request.resultFrom,
                                                               resultSize=resultSize, order=orderData)
            response = CountryAppService_statesByCountryIdResponse()
            response.itemCount = result['itemCount']
            for state in result['items']:
                response.states.add(id=state.id(), name=state.name())
            logger.debug(f'[{CountryApplicationService.statesByCountryId.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CountryAppService_statesByCountryIdResponse()
