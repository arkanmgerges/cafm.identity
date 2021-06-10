"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.resource.exception.UserDoesNotExistException import (
    UserDoesNotExistException,
)
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user.User import User
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.user_app_service_pb2 import (
    UserAppService_userByEmailAndPasswordResponse,
    UserAppService_usersResponse,
    UserAppService_userByIdResponse,
    UserAppService_newIdResponse,
)
from src.resource.proto._generated.identity.user_app_service_pb2_grpc import (
    UserAppServiceServicer,
)


class UserAppServiceListener(UserAppServiceServicer, BaseListener):
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
                f"[{UserAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            return UserAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def user_by_email_and_password(self, request, context):
        try:
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userByEmailAndPassword(email=request.email, password=request.password)
            response = UserAppService_userByEmailAndPasswordResponse()
            self._addObjectToResponse(obj=user, response=response)
            return response
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User does not exist")
            return UserAppService_userByEmailAndPasswordResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserResponse()

    """
    c4model|cb|identity:Component(identity__grpc__UserAppServiceListener__users, "Get users", "grpc listener", "Get all users")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def users(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{UserAppServiceListener.users.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)

            orderData = [{"orderBy": o.order_by, "direction": o.direction} for o in request.orders]
            result: dict = userAppService.users(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = UserAppService_usersResponse()
            for user in result["items"]:
                response.users.add(
                    id=user.id(),
                    email=user.email(),
                    # firstName=user.firstName(), lastName=user.lastName(),
                    # addressOne=user.addressOne(), addressTwo=user.addressTwo(),
                    # postalCode=user.postalCode(),
                    # avatarImage=user.avatarImage()
                )
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{UserAppServiceListener.users.__qualname__}] - response: {response}")
            return UserAppService_usersResponse(users=response.users, total_item_count=response.total_item_count)
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No users found")
            return UserAppService_usersResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserAppService_usersResponse()

    """
    c4model|cb|identity:Component(identity__grpc__UserAppServiceListener__userById, "Get user by id", "grpc listener", "Get a user by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def user_by_id(self, request, context):
        try:
            token = self._token(context)
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userById(id=request.id, token=token)
            logger.debug(f"[{UserAppServiceListener.user_by_id.__qualname__}] - response: {user}")
            response = UserAppService_userByIdResponse()
            self._addObjectToResponse(obj=user, response=response)
            return response
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User does not exist")
            return UserAppService_userByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return UserAppService_userByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: User, response: Any):
        response.user.id = obj.id()
        response.user.email = obj.email()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
