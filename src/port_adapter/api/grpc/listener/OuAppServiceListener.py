"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.OuApplicationService import OuApplicationService
from src.domain_model.ou.Ou import Ou
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.resource.proto._generated.ou_app_service_pb2 import OuAppService_ouByNameResponse
from src.resource.proto._generated.ou_app_service_pb2_grpc import OuAppServiceServicer


class OuAppServiceListener(OuAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def ouByName(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            ou: Ou = ouAppService.ouByName(name=request.name)
            return OuAppService_ouByNameResponse(id=ou.id(), name=ou.name())
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Ou does not exist')
            return OuAppService_ouByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.OuResponse()
