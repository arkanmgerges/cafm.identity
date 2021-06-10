"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.CountryApplicationService import CountryApplicationService
from src.domain_model.country.City import City
from src.domain_model.country.Country import Country
from src.domain_model.country.State import State
from src.domain_model.resource.exception.CountryDoesNotExistException import (
    CountryDoesNotExistException,
)
from src.domain_model.resource.exception.StateDoesNotExistException import (
    StateDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.country_app_service_pb2 import (
    CountryAppService_countriesResponse,
    CountryAppService_countryByIdResponse,
    CountryAppService_cityByCountryIdResponse,
    CountryAppService_stateByCountryIdAndStateIdResponse,
    CountryAppService_citiesByCountryIdResponse,
    CountryAppService_statesByCountryIdResponse,
    CountryAppService_citiesByCountryIdAndStateIdResponse,
)
from src.resource.proto._generated.identity.country_app_service_pb2_grpc import (
    CountryAppServiceServicer,
)


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

            resultSize = request.result_size if request.result_size >= 0 else 10
            logger.debug(
                f"[{CountryAppServiceListener.countries.__qualname__}] - resultFrom: {request.result_from}, resultSize: {resultSize}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            orderData = [
                {"orderBy": o.orderBy, "direction": o.direction} for o in request.orders
            ]
            result: dict = countryAppService.countries(
                resultFrom=request.result_from, resultSize=resultSize, order=orderData
            )
            response = CountryAppService_countriesResponse()
            response.total_item_count = result["totalItemCount"]
            for country in result["items"]:
                response.countries.add(
                    id=country.id(),
                    locale_code=country.localeCode(),
                    continent_code=country.continentCode(),
                    continent_name=country.continentName(),
                    country_iso_code=country.countryIsoCode(),
                    country_name=country.countryName(),
                    is_in_european_union=country.isInEuropeanUnion(),
                )
            logger.debug(
                f"[{CountryApplicationService.countries.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_countriesResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__countryById, "Get country by id", "grpc listener", "Get a country by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def country_by_id(self, request, context):
        try:

            logger.debug(
                f"[{CountryAppServiceListener.country_by_id.__qualname__}] - id: {request.id}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            country: Country = countryAppService.countryById(id=request.id)
            response = CountryAppService_countryByIdResponse()
            response.country.id = country.id()
            response.country.locale_code = country.localeCode()
            response.country.continent_code = country.continentCode()
            response.country.continent_name = country.continentName()
            response.country.country_iso_code = country.countryIsoCode()
            response.country.country_name = country.countryName()
            response.country.is_in_european_union = country.isInEuropeanUnion()
            logger.debug(
                f"[{CountryApplicationService.countryById.__qualname__}] - response: {response}"
            )
            return response
        except CountryDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("country does not exist")
            return CountryAppService_countryByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_countryByIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__citiesByCountryId, "Get cities by country id", "grpc listener", "Get cities by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cities_by_country_id(self, request, context):
        try:

            resultSize = request.result_size if request.result_size >= 0 else 10
            logger.debug(
                f"[{CountryAppServiceListener.cities_by_country_id.__qualname__}] - \ "
                f"id: {request.id},resultFrom: {request.result_from}, resultSize: {resultSize}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            orderData = [
                {"orderBy": o.orderBy, "direction": o.direction} for o in request.orders
            ]
            result: dict = countryAppService.citiesByCountryId(
                id=request.id,
                resultFrom=request.result_from,
                resultSize=resultSize,
                order=orderData,
            )
            response = CountryAppService_citiesByCountryIdResponse()
            response.total_item_count = result["totalItemCount"]
            for city in result["items"]:
                response.cities.add(
                    id=city.id(),
                    locale_code=city.localeCode(),
                    continent_code=city.continentCode(),
                    continent_name=city.continentName(),
                    country_iso_code=city.countryIsoCode(),
                    country_name=city.countryName(),
                    subdivision_one_iso_code=city.subdivisionOneIsoCode(),
                    subdivision_one_iso_name=city.subdivisionOneIsoName(),
                    city_name=city.cityName(),
                    time_zone=city.timeZone(),
                    is_in_european_union=city.isInEuropeanUnion(),
                )
            logger.debug(
                f"[{CountryApplicationService.citiesByCountryId.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_citiesByCountryIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__cityByCountryId, "Get city by country id", "grpc listener", "Get a city by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def city_by_country_id(self, request, context):
        try:
            logger.debug(
                f"[{CountryAppServiceListener.city_by_country_id.__qualname__}] - \ "
                f"country id: {request.country_id},city id: {request.city_id}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            city: City = countryAppService.cityByCountryId(
                countryId=request.country_id, cityId=request.city_id
            )

            response = CountryAppService_cityByCountryIdResponse()
            response.city.id = city.id()
            response.city.locale_code = city.localeCode()
            response.city.continent_code = city.continentCode()
            response.city.continent_name = city.continentName()
            response.city.country_iso_code = city.countryIsoCode()
            response.city.country_name = city.countryName()
            response.city.subdivision_one_iso_code = city.subdivisionOneIsoCode()
            response.city.subdivision_one_iso_name = city.subdivisionOneIsoName()
            response.city.city_name = city.cityName()
            response.city.time_zone = city.timeZone()
            response.city.is_in_european_union = city.isInEuropeanUnion()

            logger.debug(
                f"[{CountryApplicationService.cityByCountryId.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_cityByCountryIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__stateByCountryIdAndStateId, "Get state by country id and state id", "grpc listener", "Get a state by country id and state id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def state_by_country_id_and_state_id(self, request, context):
        try:
            logger.debug(
                f"[{CountryAppServiceListener.state_by_country_id_and_state_id.__qualname__}] - \ "
                f"country id: {request.country_id}, state id: {request.state_id}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            state: State = countryAppService.stateByCountryIdAndStateId(
                countryId=request.country_id,
                stateId=request.state_id,
            )

            response = CountryAppService_stateByCountryIdAndStateIdResponse()
            response.state.id = state.id()
            response.state.name = state.name()

            logger.debug(
                f"[{CountryApplicationService.stateByCountryIdAndStateId.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_stateByCountryIdAndStateIdResponse()
        except StateDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("country does not exist")
            return CountryAppService_stateByCountryIdAndStateIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CountryAppServiceListener__statesByCountryId, "Get states by country id", "grpc listener", "Get a states by country id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def states_by_country_id(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            logger.debug(
                f"[{CountryAppServiceListener.states_by_country_id.__qualname__}] - \ "
                f"id: {request.id},resultFrom: {request.result_from}, resultSize: {resultSize}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            orderData = [
                {"orderBy": o.order_by, "direction": o.direction} for o in request.orders
            ]
            result: dict = countryAppService.statesByCountryId(
                id=request.id,
                resultFrom=request.result_from,
                resultSize=resultSize,
                order=orderData,
            )
            response = CountryAppService_statesByCountryIdResponse()
            response.total_item_count = result["totalItemCount"]
            for state in result["items"]:
                response.states.add(id=state.id(), name=state.name())
            logger.debug(
                f"[{CountryApplicationService.statesByCountryId.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_statesByCountryIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cities_by_country_id_and_state_id(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            logger.debug(
                f"[{CountryAppServiceListener.cities_by_country_id_and_state_id.__qualname__}] - resultFrom: {request.result_from}, resultSize: {resultSize}"
            )
            countryAppService: CountryApplicationService = AppDi.instance.get(
                CountryApplicationService
            )

            orderData = [
                {"orderBy": o.order_by, "direction": o.direction} for o in request.orders
            ]
            result: dict = countryAppService.citiesByCountryIdAndStateId(
                countryId=request.country_id,
                stateId=request.state_id,
                resultFrom=request.result_from,
                resultSize=resultSize,
                order=orderData,
            )
            response = CountryAppService_citiesByCountryIdAndStateIdResponse()
            response.total_item_count = result["totalItemCount"]
            for city in result["items"]:
                response.cities.add(
                    id=city.id(),
                    locale_code=city.localeCode(),
                    continent_code=city.continentCode(),
                    continent_name=city.continentName(),
                    country_iso_code=city.countryIsoCode(),
                    country_name=city.countryName(),
                    subdivision_one_iso_code=city.subdivisionOneIsoCode(),
                    subdivision_one_iso_name=city.subdivisionOneIsoName(),
                    city_name=city.cityName(),
                    time_zone=city.timeZone(),
                    is_in_european_union=city.isInEuropeanUnion(),
                )
            logger.debug(
                f"[{CountryApplicationService.citiesByCountryIdAndStateId.__qualname__}] - response: {response}"
            )
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CountryAppService_citiesByCountryIdAndStateIdResponse()
