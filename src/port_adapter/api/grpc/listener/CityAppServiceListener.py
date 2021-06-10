"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.CityApplicationService import CityApplicationService
from src.domain_model.country.City import City
from src.domain_model.resource.exception.CountryDoesNotExistException import (
    CountryDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.city_app_service_pb2 import (
    CityAppService_citiesResponse,
    CityAppService_cityByIdResponse,
)
from src.resource.proto._generated.identity.city_app_service_pb2_grpc import (
    CityAppServiceServicer,
)


class CityAppServiceListener(CityAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    """
    c4model|cb|identity:Component(identity__grpc__CityAppServiceListener__cityById, "Get city by id", "grpc listener", "Get a city by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def city_by_id(self, request, context):
        try:
            logger.debug(f"[{CityAppServiceListener.city_by_id.__qualname__}] - id: {request.id}")
            cityAppService: CityApplicationService = AppDi.instance.get(CityApplicationService)

            city: City = cityAppService.cityById(id=request.id)

            response = CityAppService_cityByIdResponse()
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
            logger.debug(f"[{CityAppServiceListener.city_by_id.__qualname__}] - response: {response}")
            return response
        except CountryDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("city does not exist")
            return CityAppService_cityByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CityAppService_cityByIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__CityAppServiceListener__cities, "Get cities", "grpc listener", "Get all cities")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cities(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            logger.debug(
                f"[{CityAppServiceListener.cities.__qualname__}] - resultFrom: {request.result_from}, resultSize: {resultSize}"
            )
            cityAppService: CityApplicationService = AppDi.instance.get(CityApplicationService)

            orderData = [{"orderBy": o.order_by, "direction": o.direction} for o in request.orders]
            result: dict = cityAppService.cities(resultFrom=request.result_from, resultSize=resultSize, order=orderData)
            response = CityAppService_citiesResponse()
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
            logger.debug(f"[{CityApplicationService.cities.__qualname__}] - response: {response}")
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return CityAppService_citiesResponse()
