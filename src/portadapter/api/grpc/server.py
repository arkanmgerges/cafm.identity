# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implementation of the GRPC Seans-gRPC server."""
import threading
import time
from concurrent import futures

import grpc

import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.UserApplicationService import UserApplicationService
from src.domainmodel.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domainmodel.user.User import User
import src.portadapter.api.rest.AppDi as AppDi


class Listener(identity_pb2_grpc.UserAppServiceServicer):
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


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    identity_pb2_grpc.add_UserAppServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:9999")
    server.start()
    # try:
    #     while True:
    #         print("Server Running : threadcount %i" % (threading.active_count()))
    #         time.sleep(10)
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt")
    #     server.stop(0)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
