"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RealmApplicationService import RealmApplicationService
from src.domain_model.realm.Realm import Realm
from src.domain_model.resource.exception.RealmDoesNotExistException import (
    RealmDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.realm_app_service_pb2 import (
    RealmAppService_realmByNameResponse,
    RealmAppService_realmsResponse,
    RealmAppService_realmByIdResponse,
    RealmAppService_newIdResponse,
)
from src.resource.proto._generated.identity.realm_app_service_pb2_grpc import (
    RealmAppServiceServicer,
)


class RealmAppServiceListener(RealmAppServiceServicer, BaseListener):
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
                f"[{RealmAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            return RealmAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RealmAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def realm_by_name(self, request, context):
        try:
            token = self._token(context)
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            realm: Realm = realmAppService.realmByName(name=request.name, token=token)
            response = RealmAppService_realmByNameResponse()
            self._addObjectToResponse(obj=realm, response=response)
            return response
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Realm does not exist")
            return RealmAppService_realmByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RealmAppService_realmByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RealmResponse()

    """
    c4model|cb|identity:Component(identity__grpc__RealmAppServiceListener__realms, "Get realms", "grpc listener", "Get all realms")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def realms(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{RealmAppServiceListener.realms.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)

            orderData = [{"orderBy": o.order_by, "direction": o.direction} for o in request.orders]
            result: dict = realmAppService.realms(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = RealmAppService_realmsResponse()
            for realm in result["items"]:
                response.realms.add(id=realm.id(), name=realm.name(), realm_type=realm.realmType())
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{RealmAppServiceListener.realms.__qualname__}] - response: {response}")
            return RealmAppService_realmsResponse(realms=response.realms, total_item_count=response.total_item_count)
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No realms found")
            return RealmAppService_realmsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RealmAppService_realmsResponse()

    """
    c4model|cb|identity:Component(identity__grpc__RealmAppServiceListener__realmById, "Get realm by id", "grpc listener", "Get a realm by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def realm_by_id(self, request, context):
        try:
            token = self._token(context)
            realmAppService: RealmApplicationService = AppDi.instance.get(RealmApplicationService)
            realm: Realm = realmAppService.realmById(id=request.id, token=token)
            logger.debug(f"[{RealmAppServiceListener.realm_by_id.__qualname__}] - response: {realm}")
            response = RealmAppService_realmByIdResponse()
            self._addObjectToResponse(obj=realm, response=response)
            return response
        except RealmDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Realm does not exist")
            return RealmAppService_realmByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RealmAppService_realmByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: Realm, response: Any):
        response.realm.id = obj.id()
        response.realm.name = obj.name()
        response.realm.realm_type = obj.realmType()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
