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
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
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
            token = self._token(context)
            ou: Ou = ouAppService.ouByName(name=request.name, token=token)
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
            token = self._token(context)
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{OuAppServiceListener.ous.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)

            ous: List[Ou] = ouAppService.ous(ownedRoles=ownedRoles, resultFrom=request.resultFrom,
                                             resultSize=resultSize, token=token)
            response = OuAppService_ousResponse()
            for ou in ous:
                response.ous.add(id=ou.id(), name=ou.name())
            logger.debug(f'[{OuAppServiceListener.ous.__qualname__}] - response: {response}')
            return OuAppService_ousResponse(ous=response.ous)
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No ous found')
            return OuAppService_ouByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return OuAppService_ouByNameResponse()

    def ouById(self, request, context):
        try:
            ouAppService: OuApplicationService = AppDi.instance.get(OuApplicationService)
            token = self._token(context)
            ou: Ou = ouAppService.ouById(id=request.id, token=token)
            logger.debug(f'[{OuAppServiceListener.ouById.__qualname__}] - response: {ou}')
            response = OuAppService_ouByIdResponse()
            response.ou.id = ou.id()
            response.ou.name = ou.name()
            return response
        except OuDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Ou does not exist')
            return OuAppService_ouByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return OuAppService_ouByIdResponse()

    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''
