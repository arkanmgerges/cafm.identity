"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.OuApplicationService import OuApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.ou.Ou import Ou
from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
from src.resource.logging.logger import logger
from src.resource.proto._generated.ou_app_service_pb2 import OuAppService_ouByNameResponse, OuAppService_ousResponse, \
    OuAppService_ouByIdResponse
from src.resource.proto._generated.ou_app_service_pb2_grpc import OuAppServiceServicer


class OuAppServiceListener(OuAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def ouByName(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            ou: Ou = ouAppService.ouByName(name=request.name)
            response = OuAppService_ouByNameResponse()
            response.ou.id = ou.id()
            response.ou.name = ou.name()
            return response
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Ou does not exist')
            return OuAppService_ouByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.OuResponse()
    def ous(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedOus = claims['ou'] if 'ou' in claims else []
            logger.debug(f'[{OuAppServiceListener.ous.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedOus {ownedOus}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)

            ous: List[Ou] = ouAppService.ous(ownedOus=ownedOus, resultFrom=request.resultFrom,
                                                     resultSize=resultSize)
            response = OuAppService_ousResponse()
            for ou in ous:
                response.ous.add(id=ou.id(), name=ou.name())
            logger.debug(f'[{OuAppServiceListener.ous.__qualname__}] - response: {response}')
            return OuAppService_ousResponse(ous=response.ous)
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No ous found')
            return OuAppService_ouByNameResponse()

    def ouById(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            ou: Ou = ouAppService.ouById(id=request.id)
            logger.debug(f'[{OuAppServiceListener.ouById.__qualname__}] - response: {ou}')
            response = OuAppService_ouByIdResponse()
            response.ou.id = ou.id()
            response.ou.name = ou.name()
            return response
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Ou does not exist')
            return OuAppService_ouByIdResponse()