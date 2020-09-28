"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.RoleApplicationService import RoleApplicationService
from src.domainmodel.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domainmodel.role.Role import Role


class RoleAppServiceListener(identity_pb2_grpc.RoleAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def roleByName(self, request, context):
        try:
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name)
            return identity_pb2.RoleAppService_roleByNameResponse(id=role.id(), name=role.name())
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return identity_pb2.RoleAppService_roleByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RoleResponse()
