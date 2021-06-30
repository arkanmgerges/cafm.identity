"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException

from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry

from src.resource.proto._generated.identity.policy_app_service_pb2 import \
    PolicyAppService_usersIncludeAccessRolesResponse, \
    PolicyAppService_usersIncludeRolesResponse, PolicyAppService_usersIncludeAccessRolesResponse, \
    PolicyAppService_realmsIncludeUsersIncludeRolesResponse
from src.resource.proto._generated.identity.policy_app_service_pb2_grpc import PolicyAppServiceServicer


class PolicyAppServiceListener(PolicyAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.cpolicynter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def users_include_access_roles(self, request, context):
        response = PolicyAppService_usersIncludeAccessRolesResponse
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PolicyAppServiceListener.users_include_access_roles.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
            response = response()
            result = appService.usersIncludeAccessRoles(token=token)
            logger.debug(f"[{PolicyAppServiceListener.users_include_access_roles.__qualname__}] - app service result: {result}")
            response.total_item_count = result["totalItemCount"]
            for resultItem in result["items"]:
                responseItem = response.user_includes_roles_items.add()
                responseItem.id = resultItem.id()
                responseItem.email = resultItem.email()
                for role in resultItem.roles():
                    roleResponseItem = responseItem.roles.add()
                    roleResponseItem.id = role.id()
                    roleResponseItem.type = role.type()
                    roleResponseItem.name = role.name()
                    roleResponseItem.title = role.title()
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return response()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def users_include_roles(self, request, context):
        response = PolicyAppService_usersIncludeRolesResponse
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PolicyAppServiceListener.users_include_roles.__qualname__}] - claims: {claims}\n\t \
                        token: {token}"
            )
            appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
            response = response()
            result = appService.usersIncludeRoles(token=token)
            logger.debug(
                f"[{PolicyAppServiceListener.users_include_roles.__qualname__}] - app service result: {result}")
            response.total_item_count = result["totalItemCount"]
            for resultItem in result["items"]:
                responseItem = response.user_includes_roles_items.add()
                responseItem.id = resultItem.id()
                responseItem.email = resultItem.email()
                for role in resultItem.roles():
                    roleResponseItem = responseItem.roles.add()
                    roleResponseItem.id = role.id()
                    roleResponseItem.type = role.type()
                    roleResponseItem.name = role.name()
                    roleResponseItem.title = role.title()
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return response()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def realms_include_users_include_roles(self, request, context):
        response = PolicyAppService_realmsIncludeUsersIncludeRolesResponse
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PolicyAppServiceListener.realms_include_users_include_roles.__qualname__}] - claims: {claims}\n\t \
                            token: {token}"
            )
            appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
            response = response()
            result = appService.realmsIncludeUsersIncludeRoles(token=token)
            logger.debug(
                f"[{PolicyAppServiceListener.realms_include_users_include_roles.__qualname__}] - app service result: {result}")
            response.total_item_count = result["totalItemCount"]
            for resultItem in result["items"]:
                responseItem = response.realm_includes_users_include_roles_items.add()
                responseItem.id = resultItem.id()
                responseItem.name = resultItem.name()
                responseItem.realm_type = resultItem.realmType()
                for userIncludesRoles in resultItem.usersIncludeRoles():
                    userIncludesRolesResponseItem = responseItem.user_includes_roles.add()
                    userIncludesRolesResponseItem.id = userIncludesRoles.id()
                    userIncludesRolesResponseItem.email = userIncludesRoles.email()
                    for role in userIncludesRoles.roles():
                        roleResponseItem = userIncludesRolesResponseItem.roles.add()
                        roleResponseItem.id = role.id()
                        roleResponseItem.type = role.type()
                        roleResponseItem.name = role.name()
                        roleResponseItem.title = role.title()
            return response
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return response()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
