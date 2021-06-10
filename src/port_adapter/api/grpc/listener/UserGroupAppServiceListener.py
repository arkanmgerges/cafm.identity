"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.resource.exception.UserGroupDoesNotExistException import (
    UserGroupDoesNotExistException,
)
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user_group.UserGroup import UserGroup
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.user_group_app_service_pb2 import (
    UserGroupAppService_userGroupByNameResponse,
    UserGroupAppService_userGroupsResponse,
    UserGroupAppService_userGroupByIdResponse,
    UserGroupAppService_newIdResponse,
)
from src.resource.proto._generated.identity.user_group_app_service_pb2_grpc import (
    UserGroupAppServiceServicer,
)


class UserGroupAppServiceListener(UserGroupAppServiceServicer, BaseListener):
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
            claims = (
                self._tokenService.claimsFromToken(token=token)
                if "token" != ""
                else None
            )
            logger.debug(
                f"[{UserGroupAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: UserGroupApplicationService = AppDi.instance.get(
                UserGroupApplicationService
            )
            return UserGroupAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserGroupAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def user_group_by_name(self, request, context):
        try:
            token = self._token(context)
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(
                UserGroupApplicationService
            )
            userGroup: UserGroup = userGroupAppService.userGroupByName(
                name=request.name, token=token
            )
            response = UserGroupAppService_userGroupByNameResponse()
            self._addObjectToResponse(obj=userGroup, response=response)
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("UserGroup does not exist")
            return UserGroupAppService_userGroupByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserGroupAppService_userGroupByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserGroupResponse()

    """
    c4model|cb|identity:Component(identity__grpc__UserGroupAppServiceListener__userGroups, "Get user groups", "grpc listener", "Get all user groups")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def user_groups(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = (
                self._tokenService.claimsFromToken(token=token)
                if "token" != ""
                else None
            )
            logger.debug(
                f"[{UserGroupAppServiceListener.user_groups.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(
                UserGroupApplicationService
            )

            orderData = [
                {"orderBy": o.order_by, "direction": o.direction} for o in request.orders
            ]
            result: dict = userGroupAppService.userGroups(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = UserGroupAppService_userGroupsResponse()
            for userGroup in result["items"]:
                response.user_groups.add(id=userGroup.id(), name=userGroup.name())
            response.total_item_count = result["totalItemCount"]
            logger.debug(
                f"[{UserGroupAppServiceListener.user_groups.__qualname__}] - response: {response}"
            )
            return UserGroupAppService_userGroupsResponse(
                user_groups=response.user_groups, total_item_count=response.total_item_count
            )
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No userGroups found")
            return UserGroupAppService_userGroupsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserGroupAppService_userGroupsResponse()

    """
    c4model|cb|identity:Component(identity__grpc__UserGroupAppServiceListener__userGroupById, "Get user group by id", "grpc listener", "Get a user group by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def user_group_by_id(self, request, context):
        try:
            token = self._token(context)
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(
                UserGroupApplicationService
            )
            userGroup: UserGroup = userGroupAppService.userGroupById(
                id=request.id, token=token
            )
            logger.debug(
                f"[{UserGroupAppServiceListener.user_group_by_id.__qualname__}] - response: {userGroup}"
            )
            response = UserGroupAppService_userGroupByIdResponse()
            self._addObjectToResponse(obj=userGroup, response=response)
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("UserGroup does not exist")
            return UserGroupAppService_userGroupByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserGroupAppService_userGroupByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: UserGroup, response: Any):
        response.user_group.id = obj.id()
        response.user_group.name = obj.name()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
