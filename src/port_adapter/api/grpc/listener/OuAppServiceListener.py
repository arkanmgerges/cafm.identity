"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.OuApplicationService import OuApplicationService
from src.domain_model.ou.Ou import Ou
from src.domain_model.resource.exception.OuDoesNotExistException import (
    OuDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.ou_app_service_pb2 import (
    OuAppService_ouByNameResponse,
    OuAppService_ousResponse,
    OuAppService_ouByIdResponse,
    OuAppService_newIdResponse,
)
from src.resource.proto._generated.identity.ou_app_service_pb2_grpc import (
    OuAppServiceServicer,
)


class OuAppServiceListener(OuAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def new_id(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{OuAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            return OuAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return OuAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def ou_by_name(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            token = self._token(context)
            ou: Ou = ouAppService.ouByName(name=request.name, token=token)
            response = OuAppService_ouByNameResponse()
            self._addObjectToResponse(obj=ou, response=response)
            return response
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ou does not exist")
            return OuAppService_ouByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.OuResponse()

    """
    c4model|cb|identity:Component(identity__grpc__OuAppServiceListener__ous, "Get ous", "grpc listener", "Get all ous")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def ous(self, request, context):
        try:
            token = self._token(context)
            resultSize = request.result_size if request.result_size >= 0 else 10
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            token = self._token(context)
            logger.debug(
                f"[{OuAppServiceListener.ous.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.orders]
            result: dict = ouAppService.ous(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = OuAppService_ousResponse()
            for ou in result["items"]:
                response.ous.add(id=ou.id(), name=ou.name())
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{OuAppServiceListener.ous.__qualname__}] - response: {response}")
            return OuAppService_ousResponse(ous=response.ous, total_item_count=response.total_item_count)
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No ous found")
            return OuAppService_ousResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return OuAppService_ousResponse()

    """
    c4model|cb|identity:Component(identity__grpc__OuAppServiceListener__ouById, "Get ou by id", "grpc listener", "Get a ou by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def ou_by_id(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            token = self._token(context)
            ou: Ou = ouAppService.ouById(id=request.id, token=token)
            logger.debug(f"[{OuAppServiceListener.ou_by_id.__qualname__}] - response: {ou}")
            response = OuAppService_ouByIdResponse()
            self._addObjectToResponse(obj=ou, response=response)
            return response
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ou does not exist")
            return OuAppService_ouByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return OuAppService_ouByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: Ou, response: Any):
        response.ou.id = obj.id()
        response.ou.name = obj.name()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
