"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.permission.Permission import Permission
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.resource.proto._generated.permission_app_service_pb2 import PermissionAppService_permissionByNameResponse
from src.resource.proto._generated.permission_app_service_pb2_grpc import PermissionAppServiceServicer


class PermissionAppServiceListener(PermissionAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def permissionByName(self, request, context):
        try:
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionByName(name=request.name)
            return PermissionAppService_permissionByNameResponse(id=permission.id(), name=permission.name())
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Permission does not exist')
            return PermissionAppService_permissionByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.PermissionResponse()
