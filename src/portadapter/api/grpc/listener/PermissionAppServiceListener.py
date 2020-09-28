"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.PermissionApplicationService import PermissionApplicationService
from src.domainmodel.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domainmodel.permission.Permission import Permission


class PermissionAppServiceListener(identity_pb2_grpc.PermissionAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def permissionByName(self, request, context):
        try:
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionByName(name=request.name)
            return identity_pb2.PermissionAppService_permissionByNameResponse(id=permission.id(), name=permission.name())
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Permission does not exist')
            return identity_pb2.PermissionAppService_permissionByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.PermissionResponse()
