"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.AuthenticationApplicationService import AuthenticationApplicationService
from src.domain_model.resource.exception.InvalidCredentialsException import InvalidCredentialsException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.resource.logging.logger import logger
from src.resource.proto._generated.auth_app_service_pb2 import AuthAppService_authenticateUserByNameAndPasswordResponse, \
    AuthAppService_isAuthenticatedResponse
from src.resource.proto._generated.auth_app_service_pb2_grpc import AuthAppServiceServicer


class AuthAppServiceListener(AuthAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def authenticateUserByNameAndPassword(self, request, context):
        try:
            # logger.debug(
            # f'request: {request}\n, target: {target}\n, options: {options}\n, channel_credentials: {channel_credentials}\n insecure: {insecure}\n, compression: {compression}\n, wait_for_ready: {wait_for_ready}\n, timeout: {timeout}\n, metadata: {metadata}')
            # for key, value in context.invocation_metadata():
            #     print('Received initial metadata: key=%s value=%s' % (key, value))
            logger.debug(
                f'[{AuthAppServiceListener.authenticateUserByNameAndPassword.__qualname__}] - receive request with name: {request.name}')
            authAppService: AuthenticationApplicationService = AppDi.instance.get(AuthenticationApplicationService)
            token: str = authAppService.authenticateUserByNameAndPassword(name=request.name,
                                                                          password=request.password)
            logger.debug(
                f'[{AuthAppServiceListener.authenticateUserByNameAndPassword.__qualname__}] - token returned token: {token}')
            return AuthAppService_authenticateUserByNameAndPasswordResponse(token=token)
        except InvalidCredentialsException:
            logger.debug(
                f'[{AuthAppServiceListener.authenticateUserByNameAndPassword.__qualname__}] - exception, {InvalidCredentialsException.__qualname__}')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Invalid credentials')
            return AuthAppService_authenticateUserByNameAndPasswordResponse()
        except UserDoesNotExistException:
            logger.debug(
                f'[{AuthAppServiceListener.authenticateUserByNameAndPassword.__qualname__}] - exception, {UserDoesNotExistException.__qualname__}')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User does not exist')
            return AuthAppService_authenticateUserByNameAndPasswordResponse()
        except Exception as e:
            logger.warn(
                f'[{AuthAppServiceListener.authenticateUserByNameAndPassword.__qualname__}] - exception, Unknown: {e}')
            raise e

    # def isAuthenticated(self, request, context):
    #     metadata = context.invocation_metadata()
    #     logger.debug(f'[{AuthAppServiceListener.isAuthenticated.__qualname__}] - Getting metadata {metadata}')
    #     token = metadata[0].value if 'token' in metadata[0] else None
    #     if token is None:
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         context.set_details('Token not found')
    #         return AuthAppService_isAuthenticatedResponse()
    #     else:
    #         try:
    #             authAppService: AuthenticationApplicationService = AppDi.instance.get(AuthenticationApplicationService)
    #             result = authAppService.isAuthenticated(token=token)
    #             return AuthAppService_isAuthenticatedResponse(response=result)
    #         except Exception as e:
    #             context.set_code(grpc.StatusCode.ERROR)
    #             context.set_details(e)
    #             return AuthAppService_isAuthenticatedResponse()


    def isAuthenticated(self, request, context):
        try:
            authAppService: AuthenticationApplicationService = AppDi.instance.get(AuthenticationApplicationService)
            logger.debug(f'[{AuthAppServiceListener.isAuthenticated.__qualname__}] - Call with token: {request.token}')
            result = authAppService.isAuthenticated(token=request.token)
            logger.debug(f'[{AuthAppServiceListener.isAuthenticated.__qualname__}] - Receive response with result: {result}')
            return AuthAppService_isAuthenticatedResponse(response=result)
        except Exception as e:
            context.set_code(grpc.StatusCode.ERROR)
            context.set_details(e)
            return AuthAppService_isAuthenticatedResponse()
