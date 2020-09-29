"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.role.Role import Role
from src.resource.proto._generated.role_app_service_pb2 import RoleAppService_roleByNameResponse
from src.resource.proto._generated.role_app_service_pb2_grpc import RoleAppServiceServicer


class RoleAppServiceListener(RoleAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def roleByName(self, request, context):
        try:
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name)
            return RoleAppService_roleByNameResponse(id=role.id(), name=role.name())
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return RoleAppService_roleByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RoleResponse()
