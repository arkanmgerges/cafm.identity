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

from src.resource.proto._generated.identity.policy_app_service_pb2 import PolicyAppService_usersWithAccessRolesResponse
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
    def users_with_access_roles(self, request, context):
        response = PolicyAppService_usersWithAccessRolesResponse
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{PolicyAppServiceListener.users_with_access_roles.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
            response = response()
            result = appService.usersWithAccessRoles(token=token)
            logger.debug(f"[{PolicyAppServiceListener.users_with_access_roles.__qualname__}] - app service result: {result}")
            response.total_item_count = result["totalItemCount"]
            for resultItem in result["items"]:
                responseItem = response.user_with_roles_items.add()
                responseItem.user.id = resultItem["user"].id()
                responseItem.user.email = resultItem["user"].email()
                for role in resultItem["roles"]:
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
    def _token(self, context) -> str:
        return super()._token(context=context)
