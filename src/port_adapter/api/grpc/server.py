# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implementation of the GRPC Seans-gRPC server."""
import random
import threading
from concurrent import futures
from datetime import datetime

import grpc
from grpc_reflection.v1alpha import reflection

import src.port_adapter.AppDi as AppDi
import src.resource.proto._generated
from src.port_adapter.api.grpc.listener.AuthAppServiceListener import (
    AuthAppServiceListener,
)
from src.port_adapter.api.grpc.listener.AuthzAppServiceListener import (
    AuthzAppServiceListener,
)
from src.port_adapter.api.grpc.listener.CityAppServiceListener import (
    CityAppServiceListener,
)
from src.port_adapter.api.grpc.listener.CountryAppServiceListener import (
    CountryAppServiceListener,
)
from src.port_adapter.api.grpc.listener.OuAppServiceListener import OuAppServiceListener
from src.port_adapter.api.grpc.listener.PermissionAppServiceListener import (
    PermissionAppServiceListener,
)
from src.port_adapter.api.grpc.listener.PermissionContextAppServiceListener import (
    PermissionContextAppServiceListener,
)
from src.port_adapter.api.grpc.listener.PolicyAppServiceListener import PolicyAppServiceListener
from src.port_adapter.api.grpc.listener.ProjectAppServiceListener import (
    ProjectAppServiceListener,
)
from src.port_adapter.api.grpc.listener.RealmAppServiceListener import (
    RealmAppServiceListener,
)
from src.port_adapter.api.grpc.listener.RoleAppServiceListener import (
    RoleAppServiceListener,
)
from src.port_adapter.api.grpc.listener.UserAppServiceListener import (
    UserAppServiceListener,
)
from src.port_adapter.api.grpc.listener.UserGroupAppServiceListener import (
    UserGroupAppServiceListener,
)
from src.resource.logging.LogProcessor import LogProcessor
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.auth_app_service_pb2_grpc import (
    add_AuthAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.authz_app_service_pb2_grpc import (
    add_AuthzAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.city_app_service_pb2_grpc import (
    add_CityAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.country_app_service_pb2_grpc import (
    add_CountryAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.ou_app_service_pb2_grpc import (
    add_OuAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.permission_app_service_pb2_grpc import (
    add_PermissionAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.permission_context_app_service_pb2_grpc import (
    add_PermissionContextAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.policy_app_service_pb2_grpc import add_PolicyAppServiceServicer_to_server
from src.resource.proto._generated.identity.project_app_service_pb2_grpc import (
    add_ProjectAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.realm_app_service_pb2_grpc import (
    add_RealmAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.role_app_service_pb2_grpc import (
    add_RoleAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.user_app_service_pb2_grpc import (
    add_UserAppServiceServicer_to_server,
)
from src.resource.proto._generated.identity.user_group_app_service_pb2_grpc import (
    add_UserGroupAppServiceServicer_to_server,
)


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=1))
    add_UserAppServiceServicer_to_server(UserAppServiceListener(), server)
    add_RoleAppServiceServicer_to_server(RoleAppServiceListener(), server)
    add_UserGroupAppServiceServicer_to_server(UserGroupAppServiceListener(), server)
    add_CountryAppServiceServicer_to_server(CountryAppServiceListener(), server)
    add_CityAppServiceServicer_to_server(CityAppServiceListener(), server)
    add_PermissionContextAppServiceServicer_to_server(
        PermissionContextAppServiceListener(), server
    )
    add_ProjectAppServiceServicer_to_server(ProjectAppServiceListener(), server)
    add_PolicyAppServiceServicer_to_server(PolicyAppServiceListener(), server)
    add_RealmAppServiceServicer_to_server(RealmAppServiceListener(), server)
    add_PermissionAppServiceServicer_to_server(PermissionAppServiceListener(), server)
    add_OuAppServiceServicer_to_server(OuAppServiceListener(), server)
    add_AuthAppServiceServicer_to_server(AuthAppServiceListener(), server)
    add_AuthzAppServiceServicer_to_server(AuthzAppServiceListener(), server)

    SERVICE_NAMES = (
        src.resource.proto._generated.identity.user_app_service_pb2.DESCRIPTOR.services_by_name['UserAppService'].full_name,
        src.resource.proto._generated.identity.role_app_service_pb2.DESCRIPTOR.services_by_name['RoleAppService'].full_name,
        src.resource.proto._generated.identity.user_group_app_service_pb2.DESCRIPTOR.services_by_name['UserGroupAppService'].full_name,
        src.resource.proto._generated.identity.country_app_service_pb2.DESCRIPTOR.services_by_name['CountryAppService'].full_name,
        src.resource.proto._generated.identity.city_app_service_pb2.DESCRIPTOR.services_by_name['CityAppService'].full_name,
        src.resource.proto._generated.identity.permission_context_app_service_pb2.DESCRIPTOR.services_by_name['PermissionContextAppService'].full_name,
        src.resource.proto._generated.identity.permission_app_service_pb2.DESCRIPTOR.services_by_name['PermissionAppService'].full_name,
        src.resource.proto._generated.identity.project_app_service_pb2.DESCRIPTOR.services_by_name['ProjectAppService'].full_name,
        src.resource.proto._generated.identity.policy_app_service_pb2.DESCRIPTOR.services_by_name['PolicyAppService'].full_name,
        src.resource.proto._generated.identity.realm_app_service_pb2.DESCRIPTOR.services_by_name['RealmAppService'].full_name,
        src.resource.proto._generated.identity.ou_app_service_pb2.DESCRIPTOR.services_by_name['OuAppService'].full_name,
        src.resource.proto._generated.identity.auth_app_service_pb2.DESCRIPTOR.services_by_name['AuthAppService'].full_name,
        src.resource.proto._generated.identity.authz_app_service_pb2.DESCRIPTOR.services_by_name['AuthzAppService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    port = "[::]:9999"
    server.add_insecure_port(port)

    logger.info(f"Identity microservice grpc server started/restarted on port {port}")
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
    random.seed(datetime.utcnow().timestamp())
    openTelemetry = AppDi.instance.get(OpenTelemetry)

    # region Logger
    import src.resource.Di as Di
    logProcessor = Di.instance.get(LogProcessor)
    thread = threading.Thread(target=logProcessor.start)
    thread.start()
    # endregion

    serve()
