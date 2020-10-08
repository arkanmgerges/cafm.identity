"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
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
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name)
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
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{RoleAppServiceListener.roles.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            roles: List[Role] = roleAppService.roles(ownedRoles=ownedRoles, resultFrom=request.resultFrom,
                                                     resultSize=resultSize)
            response = RoleAppService_rolesResponse()
            for role in roles:
                response.roles.add(id=role.id(), name=role.name())
            logger.debug(f'[{RoleAppServiceListener.roles.__qualname__}] - response: {response}')
            return RoleAppService_rolesResponse(roles=response.roles)
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No roles found')
            return RoleAppService_roleByNameResponse()

    def roleById(self, request, context):
        try:
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleById(id=request.id)
            logger.debug(f'[{RoleAppServiceListener.roleById.__qualname__}] - response: {role}')
            response = RoleAppService_roleByIdResponse()
            response.role.id = role.id()
            response.role.name = role.name()
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return RoleAppService_roleByIdResponse()
