"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import src.port_adapter.AppDi as AppDi
from src.application.AuthorizationApplicationService import (
    AuthorizationApplicationService,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.proto._generated.identity.authz_app_service_pb2 import (
    AuthzAppService_hashKeysResponse,
)
from src.resource.proto._generated.identity.authz_app_service_pb2_grpc import (
    AuthzAppServiceServicer,
)
from src.resource.proto._generated.identity.hashed_key_pb2 import HashedKey


class AuthzAppServiceListener(AuthzAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    def hash_keys(self, request, context):
        try:
            authzAppService: AuthorizationApplicationService = AppDi.instance.get(
                AuthorizationApplicationService
            )
            result = authzAppService.hashKeys(
                keys=[{"key": item.key} for item in request.keys]
            )
            return AuthzAppService_hashKeysResponse(
                hashed_keys=[
                    HashedKey(key=item["key"], hash_code=item["hashCode"])
                    for item in result
                ]
            )
        except Exception as e:
            logger.warn(
                f"[{AuthzAppServiceListener.hash_keys.__qualname__}] - exception, Unknown: {e}"
            )
            raise e
