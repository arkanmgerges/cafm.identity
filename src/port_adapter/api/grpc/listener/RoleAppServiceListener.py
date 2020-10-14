"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.role.Role import Role
from src.resource.logging.logger import logger
from src.resource.proto._generated.role_app_service_pb2 import RoleAppService_roleByNameResponse, \
    RoleAppService_rolesResponse, RoleAppService_roleByIdResponse
from src.resource.proto._generated.role_app_service_pb2_grpc import RoleAppServiceServicer


class RoleAppServiceListener(RoleAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def roleByName(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name, token=token)
            response = RoleAppService_roleByNameResponse()
            response.role.id = role.id()
            response.role.name = role.name()
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return RoleAppService_roleByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RoleResponse()

    def roles(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{RoleAppServiceListener.roles.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            logger.debug(f'request: {request}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = roleAppService.roles(ownedRoles=ownedRoles,
                                                resultFrom=request.resultFrom,
                                                resultSize=resultSize,
                                                token=token,
                                                order=orderData)
            response = RoleAppService_rolesResponse()
            for role in result['items']:
                response.roles.add(id=role.id(), name=role.name())
            response.itemCount = result['itemCount']
            logger.debug(f'[{RoleAppServiceListener.roles.__qualname__}] - response: {response}')
            return RoleAppService_rolesResponse(roles=response.roles, itemCount=response.itemCount)
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No roles found')
            return RoleAppService_roleByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return RoleAppService_roleByNameResponse()

    def roleById(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleById(id=request.id, token=token)
            logger.debug(f'[{RoleAppServiceListener.roleById.__qualname__}] - response: {role}')
            response = RoleAppService_roleByIdResponse()
            response.role.id = role.id()
            response.role.name = role.name()
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return RoleAppService_roleByIdResponse()

    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        raise UnAuthorizedException()
