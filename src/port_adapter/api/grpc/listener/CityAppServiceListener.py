"""
@author: Mohammad S. moso<moso@develoop.run>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.CityApplicationService import CityApplicationService
from src.domain_model.country.City import City
from src.domain_model.resource.exception.CountryDoesNotExistException import CountryDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.city_app_service_pb2 import CityAppService_citiesResponse, \
    CityAppService_cityByIdResponse
from src.resource.proto._generated.identity.city_app_service_pb2_grpc import CityAppServiceServicer


class CityAppServiceListener(CityAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cityById(self, request, context):
        try:
            metadata = context.invocation_metadata()
            logger.debug(
                f'[{CityAppServiceListener.cityById.__qualname__}] - metadata: {metadata}\n\t id: {request.id}')
            cityAppService: CityApplicationService = AppDi.instance.get(CityApplicationService)

            city: City = cityAppService.cityById(id=request.id)

            response = CityAppService_cityByIdResponse()
            response.city.geoNameId = city.geoNameId()
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
            logger.debug(f'[{CityAppServiceListener.cityById.__qualname__}] - response: {response}')
            return response
        except CountryDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('city does not exist')
            return CityAppService_cityByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CityAppService_cityByIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def cities(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize >= 0 else 10
            logger.debug(
                f'[{CityAppServiceListener.cities.__qualname__}] - metadata: {metadata}\n\t resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            cityAppService: CityApplicationService = AppDi.instance.get(CityApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = cityAppService.cities(resultFrom=request.resultFrom, resultSize=resultSize, order=orderData)
            response = CityAppService_citiesResponse()
            response.itemCount = result['itemCount']
            for city in result['items']:
                response.cities.add(geoNameId=city.geoNameId(), localeCode=city.localeCode(),
                                    continentCode=city.continentCode(), continentName=city.continentName(),
                                    countryIsoCode=city.countryIsoCode(), countryName=city.countryName(),
                                    subdivisionOneIsoCode=city.subdivisionOneIsoCode(),
                                    subdivisionOneIsoName=city.subdivisionOneIsoName(), cityName=city.cityName(),
                                    timeZone=city.timeZone(), isInEuropeanUnion=city.isInEuropeanUnion())
            logger.debug(f'[{CityApplicationService.cities.__qualname__}] - response: {response}')
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return CityAppService_citiesResponse()
