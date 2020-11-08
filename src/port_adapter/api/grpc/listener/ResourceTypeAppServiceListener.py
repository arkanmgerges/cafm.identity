"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PermissionContextApplicationService import PermissionContextApplicationService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import PermissionContextDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.resource.logging.logger import logger
from src.resource.proto._generated.permission_context_app_service_pb2 import \
    PermissionContextAppService_permissionContextByNameResponse, PermissionContextAppService_permissionContextsResponse, \
    PermissionContextAppService_permissionContextByIdResponse
from src.resource.proto._generated.permission_context_app_service_pb2_grpc import PermissionContextAppServiceServicer


class PermissionContextAppServiceListener(PermissionContextAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def permissionContextByName(self, request, context):
        try:
            token = self._token(context)
            permissionContextAppService: PermissionContextApplicationService = AppDi.instance.get(PermissionContextApplicationService)
            permissionContext: PermissionContext = permissionContextAppService.permissionContextByName(name=request.name, token=token)
            response = PermissionContextAppService_permissionContextByNameResponse()
            response.permissionContext.id = permissionContext.id()
            response.permissionContext.name = permissionContext.name()
            return response
        except PermissionContextDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('PermissionContext does not exist')
            return PermissionContextAppService_permissionContextByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return PermissionContextAppService_permissionContextByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.PermissionContextResponse()

    def permissionContexts(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{PermissionContextAppServiceListener.permissionContexts.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            permissionContextAppService: PermissionContextApplicationService = AppDi.instance.get(PermissionContextApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = permissionContextAppService.permissionContexts(ownedRoles=ownedRoles,
                                                                resultFrom=request.resultFrom,
                                                                resultSize=resultSize,
                                                                token=token,
                                                                order=orderData)
            response = PermissionContextAppService_permissionContextsResponse()
            for permissionContext in result['items']:
                response.permissionContexts.add(id=permissionContext.id(), name=permissionContext.name())
            response.itemCount = result['itemCount']
            logger.debug(f'[{PermissionContextAppServiceListener.permissionContexts.__qualname__}] - response: {response}')
            return PermissionContextAppService_permissionContextsResponse(permissionContexts=response.permissionContexts,
                                                                itemCount=response.itemCount)
        except PermissionContextDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No permissionContexts found')
            return PermissionContextAppService_permissionContextByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return PermissionContextAppService_permissionContextByNameResponse()

    def permissionContextById(self, request, context):
        try:
            token = self._token(context)
            permissionContextAppService: PermissionContextApplicationService = AppDi.instance.get(PermissionContextApplicationService)
            permissionContext: PermissionContext = permissionContextAppService.permissionContextById(id=request.id, token=token)
            logger.debug(f'[{PermissionContextAppServiceListener.permissionContextById.__qualname__}] - response: {permissionContext}')
            response = PermissionContextAppService_permissionContextByIdResponse()
            response.permissionContext.id = permissionContext.id()
            response.permissionContext.name = permissionContext.name()
            return response
        except PermissionContextDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('PermissionContext does not exist')
            return PermissionContextAppService_permissionContextByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return PermissionContextAppService_permissionContextByIdResponse()

    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''
