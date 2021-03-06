"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.permission.Permission import Permission
from src.domain_model.resource.exception.PermissionDoesNotExistException import (
    PermissionDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.permission_app_service_pb2 import (
    PermissionAppService_permissionByNameResponse,
    PermissionAppService_permissionsResponse,
    PermissionAppService_permissionByIdResponse,
    PermissionAppService_newIdResponse, PermissionAppService_idByStringResponse,
)
from src.resource.proto._generated.identity.permission_app_service_pb2_grpc import (
    PermissionAppServiceServicer,
)


class PermissionAppServiceListener(PermissionAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def id_by_string(self, request, context):
        response = PermissionAppService_idByStringResponse
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PermissionAppServiceListener.id_by_string.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            return response(id=appService.idByString(string=request.string))
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return response()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def new_id(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PermissionAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            return PermissionAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def permission_by_name(self, request, context):
        try:
            token = self._token(context)
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionByName(name=request.name, token=token)
            response = PermissionAppService_permissionByNameResponse()
            self._addObjectToResponse(obj=permission, response=response)
            return response
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Permission does not exist")
            return PermissionAppService_permissionByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionAppService_permissionByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.PermissionResponse()

    """
    c4model|cb|identity:Component(identity__grpc__PermissionAppServiceListener__permissions, "Get permission", "grpc listener", "Get all permissions")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def permissions(self, request, context):
        try:

            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PermissionAppServiceListener.permissions.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)

            orderData = [{"orderBy": o.order_by, "direction": o.direction} for o in request.orders]
            result: dict = permissionAppService.permissions(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = PermissionAppService_permissionsResponse()
            for permission in result["items"]:
                p = response.permissions.add()
                p.id = permission.id()
                p.name = permission.name()
                for allowedAction in permission.allowedActions():
                    p.allowed_actions.append(allowedAction)
                for deniedAction in permission.deniedActions():
                    p.denied_actions.append(deniedAction)
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{PermissionAppServiceListener.permissions.__qualname__}] - response: {response}")
            return PermissionAppService_permissionsResponse(
                permissions=response.permissions, total_item_count=response.total_item_count
            )
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No permissions found")
            return PermissionAppService_permissionsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionAppService_permissionsResponse()

    """
    c4model|cb|identity:Component(identity__grpc__PermissionAppServiceListener__permissionById, "Get permission by id", "grpc listener", "Get a permission by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def permission_by_id(self, request, context):
        try:
            token = self._token(context)
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionById(id=request.id, token=token)
            logger.debug(f"[{PermissionAppServiceListener.permission_by_id.__qualname__}] - response: {permission}")
            response = PermissionAppService_permissionByIdResponse()
            self._addObjectToResponse(obj=permission, response=response)
            return response
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Permission does not exist")
            return PermissionAppService_permissionByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return PermissionAppService_permissionByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: Permission, response: Any):
        response.permission.id = obj.id()
        response.permission.name = obj.name()
        for allowedAction in obj.allowedActions():
            response.permission.allowed_actions.append(allowedAction)
        for deniedAction in obj.deniedActions():
            response.permission.denied_actions.append(deniedAction)

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
