"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.resource.logging.logger import logger
from src.resource.proto._generated.user_app_service_pb2 import UserAppService_userByNameAndPasswordResponse, \
    UserAppService_usersResponse, UserAppService_userByIdResponse
from src.resource.proto._generated.user_app_service_pb2_grpc import UserAppServiceServicer


class UserAppServiceListener(UserAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def userByNameAndPassword(self, request, context):
        try:
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userByNameAndPassword(name=request.name,
                                                              password=request.password)
            response = UserAppService_userByNameAndPasswordResponse()
            response.user.id = user.id()
            response.user.name = user.name()
            return response
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User does not exist')
            return UserAppService_userByNameAndPasswordResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserResponse()

    def users(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{UserAppServiceListener.users.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)

            users: List[User] = userAppService.users(ownedRoles=ownedRoles, resultFrom=request.resultFrom,
                                                     resultSize=resultSize)
            response = UserAppService_usersResponse()
            for user in users:
                response.users.add(id=user.id(), name=user.name())
            logger.debug(f'[{UserAppServiceListener.users.__qualname__}] - response: {response}')
            return UserAppService_usersResponse(users=response.users)
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No users found')
            return UserAppService_usersResponse()

    def userById(self, request, context):
        try:
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userById(id=request.id)
            logger.debug(f'[{UserAppServiceListener.userById.__qualname__}] - response: {user}')
            response = UserAppService_userByIdResponse()
            response.user.id = user.id()
            response.user.name = user.name()
            return response
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User does not exist')
            return UserAppService_userByIdResponse()
