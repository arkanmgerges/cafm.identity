"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.OuApplicationService import OuApplicationService
from src.domainmodel.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.domainmodel.ou.Ou import Ou


class OuAppServiceListener(identity_pb2_grpc.OuAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def ouByName(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            ou: Ou = ouAppService.ouByName(name=request.name)
            return identity_pb2.OuAppService_ouByNameResponse(id=ou.id(), name=ou.name())
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Ou does not exist')
            return identity_pb2.OuAppService_ouByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.OuResponse()
