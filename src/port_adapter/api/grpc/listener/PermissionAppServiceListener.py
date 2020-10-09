"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.permission.Permission import Permission
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.resource.logging.logger import logger
from src.resource.proto._generated.permission_app_service_pb2 import PermissionAppService_permissionByNameResponse, \
    PermissionAppService_permissionsResponse, PermissionAppService_permissionByIdResponse
from src.resource.proto._generated.permission_app_service_pb2_grpc import PermissionAppServiceServicer


class PermissionAppServiceListener(PermissionAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def permissionByName(self, request, context):
        try:
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionByName(name=request.name)
            response = PermissionAppService_permissionByNameResponse()
            response.permission.id = permission.id()
            response.permission.name = permission.name()
            return response
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Permission does not exist')
            return PermissionAppService_permissionByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.PermissionResponse()

    def permissions(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{PermissionAppServiceListener.permissions.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)

            permissions: List[Permission] = permissionAppService.permissions(ownedRoles=ownedRoles,
                                                                             resultFrom=request.resultFrom,
                                                                             resultSize=resultSize)
            response = PermissionAppService_permissionsResponse()
            for permission in permissions:
                response.permissions.add(id=permission.id(), name=permission.name())
            logger.debug(f'[{PermissionAppServiceListener.permissions.__qualname__}] - response: {response}')
            return PermissionAppService_permissionsResponse(permissions=response.permissions)
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No permissions found')
            return PermissionAppService_permissionByNameResponse()

    def permissionById(self, request, context):
        try:
            permissionAppService: PermissionApplicationService = AppDi.instance.get(PermissionApplicationService)
            permission: Permission = permissionAppService.permissionById(id=request.id)
            logger.debug(f'[{PermissionAppServiceListener.permissionById.__qualname__}] - response: {permission}')
            response = PermissionAppService_permissionByIdResponse()
            response.permission.id = permission.id()
            response.permission.name = permission.name()
            return response
        except PermissionDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Permission does not exist')
            return PermissionAppService_permissionByIdResponse()
