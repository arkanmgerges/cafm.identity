"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time
from typing import List, Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.RoleDoesNotExistException import (
    RoleDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.role_app_service_pb2 import (
    RoleAppService_roleByNameResponse,
    RoleAppService_rolesResponse,
    RoleAppService_roleByIdResponse,
    RoleAppService_rolesTreesResponse,
    RoleAppService_newIdResponse,
)
from src.resource.proto._generated.identity.role_app_service_pb2_grpc import (
    RoleAppServiceServicer,
)


class RoleAppServiceListener(RoleAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def new_id(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{RoleAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            return RoleAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RoleAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def role_by_name(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleByName(name=request.name, token=token)
            response = RoleAppService_roleByNameResponse()
            self._addObjectToResponse(obj=role, response=response)
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Role does not exist")
            return RoleAppService_roleByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.RoleResponse()

    """
    c4model|cb|identity:Component(identity__grpc__RoleAppServiceListener__roles, "Get roles", "grpc listener", "Get all roles")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roles(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{RoleAppServiceListener.roles.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            logger.debug(f"request: {request}")
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            orderData = [{"orderBy": o.order_by, "direction": o.direction} for o in request.orders]
            result: dict = roleAppService.roles(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = RoleAppService_rolesResponse()
            for role in result["items"]:
                response.roles.add(id=role.id(), type=role.type(), name=role.name(), title=role.title())
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{RoleAppServiceListener.roles.__qualname__}] - response: {response}")
            return RoleAppService_rolesResponse(roles=response.roles, total_item_count=response.total_item_count)
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No roles found")
            return RoleAppService_rolesResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return RoleAppService_rolesResponse()

    """
    c4model|cb|identity:Component(identity__grpc__RoleAppServiceListener__roleById, "Get role by id", "grpc listener", "Get a role by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def role_by_id(self, request, context):
        try:
            token = self._token(context)
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
            role: Role = roleAppService.roleById(id=request.id, token=token)
            logger.debug(f"[{RoleAppServiceListener.role_by_id.__qualname__}] - response: {role}")
            response = RoleAppService_roleByIdResponse()
            self._addObjectToResponse(obj=role, response=response)
            return response
        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Role does not exist")
            return RoleAppService_roleByIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def role_tree(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(f"[{RoleAppServiceListener.role_tree.__qualname__}] - claims: {claims}\n\t token: {token}")
            logger.debug(f"request: {request}")
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            roleAccessPermissionItem: RoleAccessPermissionData = roleAppService.roleTree(
                roleId=request.role_id, token=token
            )

            response = RoleAppService_rolesTreesResponse()
            # Create a response item
            roleAccessPermissionResponse = response.role_access_permission.add()

            # role
            self._addObjectToResponse(obj=roleAccessPermissionItem.role, response=roleAccessPermissionResponse)

            # owned by
            if roleAccessPermissionItem.ownedBy is not None:
                roleAccessPermissionResponse.owned_by.id = roleAccessPermissionItem.ownedBy.id()
                roleAccessPermissionResponse.owned_by.type = roleAccessPermissionItem.ownedBy.type()
            else:
                roleAccessPermissionItem.ownedBy = None

            # owner of
            for ownerOf in roleAccessPermissionItem.ownerOf:
                tmp = roleAccessPermissionResponse.owner_of.add()
                tmp.id = ownerOf.id()
                tmp.type = ownerOf.type()

            # permission with permission contexts
            self._populatePermissionWithPermissionContexts(
                roleAccessPermissionResponse.permission_with_permission_contexts,
                roleAccessPermissionItem.permissions,
            )

            # access tree
            self._populateAccessTree(
                roleAccessPermissionResponse.access_tree,
                roleAccessPermissionItem.accessTree,
            )

            logger.debug(f"[{RoleAppServiceListener.role_tree.__qualname__}] - response: {response}")
            return response

        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No roles found")
            return RoleAppService_roleByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
        return RoleAppService_roleByNameResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def roles_trees(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(f"[{RoleAppServiceListener.roles_trees.__qualname__}] - claims: {claims}\n\t token: {token}")
            logger.debug(f"request: {request}")
            roleAppService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

            result: List[RoleAccessPermissionData] = roleAppService.rolesTrees(token=token)
            ff = [item.toMap() for item in result]
            import zlib
            import pickle
            xx = zlib.compress(pickle.dumps(ff))
            response = RoleAppService_rolesTreesResponse(data=xx)
            return response
            for roleAccessPermissionItem in result:
                # Create a response item
                roleAccessPermissionResponse = response.role_access_permission.add()

                # role
                self._addObjectToResponse(
                    obj=roleAccessPermissionItem.role,
                    response=roleAccessPermissionResponse,
                )

                # owned by
                if roleAccessPermissionItem.ownedBy is not None:
                    roleAccessPermissionResponse.owned_by.id = roleAccessPermissionItem.ownedBy.id()
                    roleAccessPermissionResponse.owned_by.type = roleAccessPermissionItem.ownedBy.type()
                else:
                    roleAccessPermissionItem.ownedBy = None

                # owner of
                for ownerOf in roleAccessPermissionItem.ownerOf:
                    tmp = roleAccessPermissionResponse.owner_of.add()
                    tmp.id = ownerOf.id()
                    tmp.type = ownerOf.type()

                # permission with permission contexts
                self._populatePermissionWithPermissionContexts(
                    roleAccessPermissionResponse.permission_with_permission_contexts,
                    roleAccessPermissionItem.permissions,
                )

                # access tree
                self._populateAccessTree(
                    roleAccessPermissionResponse.access_tree,
                    roleAccessPermissionItem.accessTree,
                )
            raise Exception(f'ddd: {time.perf_counter()-st}')
            logger.debug(f"[{RoleAppServiceListener.roles_trees.__qualname__}] - response: {response}")
            return response

        except RoleDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No roles found")
            return RoleAppService_roleByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
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
                self._populatePermissionContext(tmp.permission_contexts.add(), permissionContext)

    @debugLogger
    def _populateData(self, protoBuf, data):
        protoBuf.data.content_type = data.contentType.value
        protoBuf.data.context = json.dumps(data.context)
        protoBuf.data.content = json.dumps(data.content.toMap())

    @debugLogger
    def _populatePermission(self, protoBuf, permission):
        protoBuf.id = permission.id()
        protoBuf.name = permission.name()
        for action in permission.allowedActions():
            protoBuf.allowed_actions.append(action)
        for action in permission.deniedActions():
            protoBuf.denied_actions.append(action)

    @debugLogger
    def _populatePermissionContext(self, protoBuf, permissionContext):
        protoBuf.id = permissionContext.id()
        protoBuf.type = permissionContext.type()
        protoBuf.data = json.dumps(permissionContext.data())

    @debugLogger
    def _addObjectToResponse(self, obj: Role, response: Any):
        response.role.id = obj.id()
        response.role.type = obj.type()
        response.role.name = obj.name()
        response.role.title = obj.title()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
