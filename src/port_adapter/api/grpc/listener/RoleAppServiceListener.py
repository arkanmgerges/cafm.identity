"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.role_app_service_pb2 import RoleAppService_roleByNameResponse, \
    RoleAppService_rolesResponse, RoleAppService_roleByIdResponse, RoleAppService_rolesTreesResponse
from src.resource.proto._generated.role_app_service_pb2_grpc import RoleAppServiceServicer


class RoleAppServiceListener(RoleAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roleByName(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name, token=token)
            response = RoleAppService_roleByNameResponse()
            response.role.id = role.id()
            response.role.type = role.type()
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

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roles(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{RoleAppServiceListener.roles.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            logger.debug(f'request: {request}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = roleAppService.roles(
                resultFrom=request.resultFrom,
                resultSize=resultSize,
                token=token,
                order=orderData)
            response = RoleAppService_rolesResponse()
            for role in result['items']:
                response.roles.add(id=role.id(), type=role.type(), name=role.name())
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

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roleById(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleById(id=request.id, token=token)
            logger.debug(f'[{RoleAppServiceListener.roleById.__qualname__}] - response: {role}')
            response = RoleAppService_roleByIdResponse()
            response.role.id = role.id()
            response.role.type = role.type()
            response.role.name = role.name()
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role does not exist')
            return RoleAppService_roleByIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roleTree(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{RoleAppServiceListener.roleTree.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t token: {token}')
            logger.debug(f'request: {request}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            roleAccessPermissionItem: RoleAccessPermissionData = roleAppService.roleTree(roleId=request.roleId, token=token)

            response = RoleAppService_rolesTreesResponse()
            # Create a response item
            roleAccessPermissionResponse = response.roleAccessPermission.add()

            # role
            roleAccessPermissionResponse.role.id = roleAccessPermissionItem.role.id()
            roleAccessPermissionResponse.role.type = roleAccessPermissionItem.role.type()
            roleAccessPermissionResponse.role.name = roleAccessPermissionItem.role.name()

            # owned by
            if roleAccessPermissionItem.ownedBy is not None:
                roleAccessPermissionResponse.ownedBy.id = roleAccessPermissionItem.ownedBy.id()
                roleAccessPermissionResponse.ownedBy.type = roleAccessPermissionItem.ownedBy.type()
            else:
                roleAccessPermissionItem.ownedBy = None

            # owner of
            for ownerOf in roleAccessPermissionItem.ownerOf:
                tmp = roleAccessPermissionResponse.ownerOf.add()
                tmp.id = ownerOf.id()
                tmp.type = ownerOf.type()

            # permission with permission contexts
            self._populatePermissionWithPermissionContexts(
                roleAccessPermissionResponse.permissionWithPermissionContexts, roleAccessPermissionItem.permissions)

            # access tree
            self._populateAccessTree(roleAccessPermissionResponse.accessTree, roleAccessPermissionItem.accessTree)

            logger.debug(f'[{RoleAppServiceListener.roleTree.__qualname__}] - response: {response}')
            return response

        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No roles found')
            return RoleAppService_roleByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
        return RoleAppService_roleByNameResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def rolesTrees(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{RoleAppServiceListener.rolesTrees.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t token: {token}')
            logger.debug(f'request: {request}')
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            result: List[RoleAccessPermissionData] = roleAppService.rolesTrees(token=token)

            response = RoleAppService_rolesTreesResponse()
            for roleAccessPermissionItem in result:
                # Create a response item
                roleAccessPermissionResponse = response.roleAccessPermission.add()

                # role
                roleAccessPermissionResponse.role.id = roleAccessPermissionItem.role.id()
                roleAccessPermissionResponse.role.type = roleAccessPermissionItem.role.type()
                roleAccessPermissionResponse.role.name = roleAccessPermissionItem.role.name()

                # owned by
                if roleAccessPermissionItem.ownedBy is not None:
                    roleAccessPermissionResponse.ownedBy.id = roleAccessPermissionItem.ownedBy.id()
                    roleAccessPermissionResponse.ownedBy.type = roleAccessPermissionItem.ownedBy.type()
                else:
                    roleAccessPermissionItem.ownedBy = None

                # owner of
                for ownerOf in roleAccessPermissionItem.ownerOf:
                    tmp = roleAccessPermissionResponse.ownerOf.add()
                    tmp.id = ownerOf.id()
                    tmp.type = ownerOf.type()

                # permission with permission contexts
                self._populatePermissionWithPermissionContexts(
                    roleAccessPermissionResponse.permissionWithPermissionContexts, roleAccessPermissionItem.permissions)

                # access tree
                self._populateAccessTree(roleAccessPermissionResponse.accessTree, roleAccessPermissionItem.accessTree)

            logger.debug(f'[{RoleAppServiceListener.rolesTrees.__qualname__}] - response: {response}')
            return response

        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No roles found')
            return RoleAppService_roleByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
        return RoleAppService_roleByNameResponse()

    @debugLogger
    def _populateAccessTree(self, protoBuf, accessTree: List[AccessNode]):
        for accessNode in accessTree:
            tmp = protoBuf.add()
            self._populateData(tmp, accessNode.data)
            self._populateAccessTree(tmp.children, accessNode.children)

    @debugLogger
    def _populatePermissionWithPermissionContexts(self, protoBuf, permissionWithPermissionContexts):
        for permissionWithPermissionContext in permissionWithPermissionContexts:
            tmp = protoBuf.add()
            self._populatePermission(tmp.permission, permissionWithPermissionContext.permission)
            for permissionContext in permissionWithPermissionContext.permissionContexts:
                self._populatePermissionContext(tmp.permissionContexts.add(), permissionContext)

    @debugLogger
    def _populateData(self, protoBuf, data):
        protoBuf.data.contentType = data.contentType.value
        protoBuf.data.context = json.dumps(data.context)
        protoBuf.data.content = json.dumps(data.content.toMap())

    @debugLogger
    def _populatePermission(self, protoBuf, permission):
        protoBuf.id = permission.id()
        protoBuf.name = permission.name()
        for action in permission.allowedActions():
            protoBuf.allowedActions.append(action)
        for action in permission.deniedActions():
            protoBuf.deniedActions.append(action)

    @debugLogger
    def _populatePermissionContext(self, protoBuf, permissionContext):
        protoBuf.id = permissionContext.id()
        protoBuf.type = permissionContext.type()
        protoBuf.data = json.dumps(permissionContext.data())

    @debugLogger
    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        raise UnAuthorizedException()
