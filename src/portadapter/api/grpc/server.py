# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implementation of the GRPC Seans-gRPC server."""
from concurrent import futures

import grpc

from src.portadapter.api.grpc.listener.OuAppServiceListener import OuAppServiceListener
from src.portadapter.api.grpc.listener.PermissionAppServiceListener import PermissionAppServiceListener
from src.portadapter.api.grpc.listener.ProjectAppServiceListener import ProjectAppServiceListener
from src.portadapter.api.grpc.listener.RealmAppServiceListener import RealmAppServiceListener
from src.portadapter.api.grpc.listener.ResourceTypeAppServiceListener import ResourceTypeAppServiceListener
from src.portadapter.api.grpc.listener.RoleAppServiceListener import RoleAppServiceListener
from src.portadapter.api.grpc.listener.UserAppServiceListener import UserAppServiceListener
from src.portadapter.api.grpc.listener.UserGroupAppServiceListener import UserGroupAppServiceListener
from src.resource.proto._generated.ou_app_service_pb2_grpc import add_OuAppServiceServicer_to_server
from src.resource.proto._generated.permission_app_service_pb2_grpc import add_PermissionAppServiceServicer_to_server
from src.resource.proto._generated.project_app_service_pb2_grpc import add_ProjectAppServiceServicer_to_server
from src.resource.proto._generated.realm_app_service_pb2_grpc import add_RealmAppServiceServicer_to_server
from src.resource.proto._generated.resource_type_app_service_pb2_grpc import \
    add_ResourceTypeAppServiceServicer_to_server
from src.resource.proto._generated.role_app_service_pb2_grpc import add_RoleAppServiceServicer_to_server
from src.resource.proto._generated.user_app_service_pb2_grpc import add_UserAppServiceServicer_to_server
from src.resource.proto._generated.user_group_app_service_pb2_grpc import add_UserGroupAppServiceServicer_to_server


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_UserAppServiceServicer_to_server(UserAppServiceListener(), server)
    add_RoleAppServiceServicer_to_server(RoleAppServiceListener(), server)
    add_UserGroupAppServiceServicer_to_server(UserGroupAppServiceListener(), server)
    add_ResourceTypeAppServiceServicer_to_server(ResourceTypeAppServiceListener(), server)
    add_ProjectAppServiceServicer_to_server(ProjectAppServiceListener(), server)
    add_RealmAppServiceServicer_to_server(RealmAppServiceListener(), server)
    add_PermissionAppServiceServicer_to_server(PermissionAppServiceListener(), server)
    add_OuAppServiceServicer_to_server(OuAppServiceListener(), server)
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
