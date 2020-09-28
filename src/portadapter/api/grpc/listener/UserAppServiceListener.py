"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.UserApplicationService import UserApplicationService
from src.domainmodel.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domainmodel.user.User import User


class UserAppServiceListener(identity_pb2_grpc.UserAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def userByUsernameAndPassword(self, request, context):
        try:
            userAppService: UserApplicationService = AppDi.instance.get(UserApplicationService)
            user: User = userAppService.userByUsernameAndPassword(username=request.username,
                                                                  password=request.password)
            return identity_pb2.UserAppService_userByUsernameAndPasswordResponse(id=user.id(), username=user.username(),
                                                                                 password=user.password())
        except UserDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User does not exist')
            return identity_pb2.UserAppService_userByUsernameAndPasswordResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserResponse()
