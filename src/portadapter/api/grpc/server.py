# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implementation of the GRPC Seans-gRPC server."""
from concurrent import futures

import grpc

import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.portadapter.api.grpc.listener.OuAppServiceListener import OuAppServiceListener
from src.portadapter.api.grpc.listener.RealmAppServiceListener import RealmAppServiceListener
from src.portadapter.api.grpc.listener.RoleAppServiceListener import RoleAppServiceListener
from src.portadapter.api.grpc.listener.UserAppServiceListener import UserAppServiceListener


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    identity_pb2_grpc.add_UserAppServiceServicer_to_server(UserAppServiceListener(), server)
    identity_pb2_grpc.add_RoleAppServiceServicer_to_server(RoleAppServiceListener(), server)
    identity_pb2_grpc.add_RealmAppServiceServicer_to_server(RealmAppServiceListener(), server)
    identity_pb2_grpc.add_OuAppServiceServicer_to_server(OuAppServiceListener(), server)
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
