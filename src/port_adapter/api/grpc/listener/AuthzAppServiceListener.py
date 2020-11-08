"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import src.port_adapter.AppDi as AppDi
from src.application.AuthorizationApplicationService import AuthorizationApplicationService
from src.resource.logging.logger import logger
from src.resource.proto._generated.authz_app_service_pb2 import AuthzAppService_isAllowedResponse
from src.resource.proto._generated.authz_app_service_pb2_grpc import AuthzAppServiceServicer


class AuthzAppServiceListener(AuthzAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def isAllowed(self, request, context):
        try:
            # logger.debug(
            # f'request: {request}\n, target: {target}\n, options: {options}\n, channel_credentials: {channel_credentials}\n insecure: {insecure}\n, compression: {compression}\n, wait_for_ready: {wait_for_ready}\n, timeout: {timeout}\n, metadata: {metadata}')
            # for key, value in context.invocation_metadata():
            #     print('Received initial metadata: key=%s value=%s' % (key, value))
            logger.debug(
                f'[{AuthzAppServiceListener.isAllowed.__qualname__}] - receive request with token: {request.token}, data: {request.data}')
            authzAppService: AuthorizationApplicationService = AppDi.instance.get(AuthorizationApplicationService)
            isAllowed: bool = authzAppService.isAllowed(token=request.token, action=request.action, permissionContext=request.permission_context, resourceId=request.resource_id)
            logger.debug(
                f'[{AuthzAppServiceListener.isAllowed.__qualname__}] - returned isAllowed: {isAllowed}')
            return AuthzAppService_isAllowedResponse(isAllowed=isAllowed)
        except Exception as e:
            logger.warn(
                f'[{AuthzAppServiceListener.isAllowed.__qualname__}] - exception, Unknown: {e}')
            raise e
