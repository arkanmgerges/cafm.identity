"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.user.User import User
from src.resource.logging.logger import logger
from src.resource.proto._generated.user_app_service_pb2 import UserAppService_userByUsernameAndPasswordResponse
from src.resource.proto._generated.user_app_service_pb2_grpc import UserAppServiceServicer


class UserAppServiceListener(UserAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def userByUsernameAndPassword(self, request, context):
        try:
            # logger.debug(
                # f'request: {request}\n, target: {target}\n, options: {options}\n, channel_credentials: {channel_credentials}\n insecure: {insecure}\n, compression: {compression}\n, wait_for_ready: {wait_for_ready}\n, timeout: {timeout}\n, metadata: {metadata}')
            # for key, value in context.invocation_metadata():
            #     print('Received initial metadata: key=%s value=%s' % (key, value))

            logger.info('test')
            authToken: list = list(map(lambda x: x[1], filter(lambda x: x[0] == 'auth_token', list(context.invocation_metadata()))))
            if len(authToken) > 0:
                logger.info(authToken)
            else:
                logger.info('Un authenticated')

            context.set_trailing_metadata((
                ('checksum-bin', b'I agree'),
                ('retry', 'false'),
            ))


            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userByUsernameAndPassword(username=request.username,
                                                                  password=request.password)
            return UserAppService_userByUsernameAndPasswordResponse(id=user.id(), username=user.username())
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User does not exist')
            return UserAppService_userByUsernameAndPasswordResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserResponse()
