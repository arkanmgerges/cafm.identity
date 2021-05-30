"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PermissionContextApplicationService import (
    PermissionContextApplicationService,
)
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import (
    PermissionContextDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.permission_context_app_service_pb2 import (
    PermissionContextAppService_permissionContextsResponse,
    PermissionContextAppService_permissionContextByIdResponse,
    PermissionContextAppService_newIdResponse,
)
from src.resource.proto._generated.identity.permission_context_app_service_pb2_grpc import (
    PermissionContextAppServiceServicer,
)


class PermissionContextAppServiceListener(PermissionContextAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def newId(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PermissionContextAppServiceListener.newId.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: PermissionContextApplicationService = AppDi.instance.get(PermissionContextApplicationService)
            return PermissionContextAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionContextAppService_newIdResponse()

    """
    c4model|cb|identity:Component(identity__grpc__PermissionContextAppServiceListener__permissionContexts, "Get permission contexts", "grpc listener", "Get all permission contexts")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def permissionContexts(self, request, context):
        try:
            resultSize = request.resultSize if request.resultSize >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None

            logger.debug(
                f"[{PermissionContextAppServiceListener.permissionContexts.__qualname__}] - \
                claims: {claims}\n\t resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}"
            )
            permissionContextAppService: PermissionContextApplicationService = AppDi.instance.get(
                PermissionContextApplicationService
            )

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = permissionContextAppService.permissionContexts(
                resultFrom=request.resultFrom,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = PermissionContextAppService_permissionContextsResponse()
            for permissionContext in result["items"]:
                response.permissionContexts.add(
                    id=permissionContext.id(),
                    type=permissionContext.type(),
                    data=json.dumps(permissionContext.data()),
                )
            response.totalItemCount = result["totalItemCount"]
            logger.debug(
                f"[{PermissionContextAppServiceListener.permissionContexts.__qualname__}] - response: {response}"
            )
            return PermissionContextAppService_permissionContextsResponse(
                permissionContexts=response.permissionContexts,
                totalItemCount=response.totalItemCount,
            )
        except PermissionContextDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No permissionContexts found")
            return PermissionContextAppService_permissionContextsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionContextAppService_permissionContextsResponse()

    """
    c4model|cb|identity:Component(identity__grpc__PermissionContextAppServiceListener__permissionContextById, "Get permission context by id", "grpc listener", "Get a permission context by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def permissionContextById(self, request, context):
        try:
            token = self._token(context)
            permissionContextAppService: PermissionContextApplicationService = AppDi.instance.get(
                PermissionContextApplicationService
            )
            permissionContext: PermissionContext = permissionContextAppService.permissionContextById(
                id=request.id, token=token
            )
            logger.debug(
                f"[{PermissionContextAppServiceListener.permissionContextById.__qualname__}] - response: \
                    {permissionContext}"
            )
            response = PermissionContextAppService_permissionContextByIdResponse()
            self._addObjectResponse(obj=permissionContext, response=response)
            return response
        except PermissionContextDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("PermissionContext does not exist")
            return PermissionContextAppService_permissionContextByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionContextAppService_permissionContextByIdResponse()

    @debugLogger
    def _addObjectResponse(self, obj: PermissionContext, response: Any):
        response.permissionContext.id = obj.id()
        response.permissionContext.type = obj.type()
        response.permissionContext.data = json.dumps(obj.data())

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
