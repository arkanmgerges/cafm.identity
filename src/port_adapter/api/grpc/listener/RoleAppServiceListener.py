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
    RoleAppService_rolesResponse
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
            return RoleAppService_roleByNameResponse(id=role.id(), name=role.name())
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
            logger.debug(f'[{RoleAppServiceListener.roles.__qualname__}] - Getting metadata {metadata}')
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(f'[{RoleAppServiceListener.roles.__qualname__}] - claims {claims}')
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(f'[{RoleAppServiceListener.roles.__qualname__}] - ownedRoles {ownedRoles}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            roles: List[Role] = roleAppService.roles(ownedRoles=ownedRoles, resultFrom=request.resultFrom,
                                                     resultSize=request.resultSize)
            return RoleAppService_rolesResponse(response=json.dumps([role.toMap() for role in roles]))
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No roles found')
            return RoleAppService_roleByNameResponse()
