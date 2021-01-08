"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.user_group_app_service_pb2 import UserGroupAppService_userGroupByNameResponse, \
    UserGroupAppService_userGroupsResponse, UserGroupAppService_userGroupByIdResponse
from src.resource.proto._generated.identity.user_group_app_service_pb2_grpc import UserGroupAppServiceServicer


class UserGroupAppServiceListener(UserGroupAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def userGroupByName(self, request, context):
        try:
            token = self._token(context)
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupByName(name=request.name, token=token)
            response = UserGroupAppService_userGroupByNameResponse()
            response.userGroup.id = userGroup.id()
            response.userGroup.name = userGroup.name()
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return UserGroupAppService_userGroupByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return UserGroupAppService_userGroupByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserGroupResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def userGroups(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize >= 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{UserGroupAppServiceListener.userGroups.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = userGroupAppService.userGroups(
                                                          resultFrom=request.resultFrom,
                                                          resultSize=resultSize,
                                                          token=token,
                                                          order=orderData)
            response = UserGroupAppService_userGroupsResponse()
            for userGroup in result['items']:
                response.userGroups.add(id=userGroup.id(), name=userGroup.name())
            response.itemCount = result['itemCount']
            logger.debug(f'[{UserGroupAppServiceListener.userGroups.__qualname__}] - response: {response}')
            return UserGroupAppService_userGroupsResponse(userGroups=response.userGroups, itemCount=response.itemCount)
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No userGroups found')
            return UserGroupAppService_userGroupsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return UserGroupAppService_userGroupsResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def userGroupById(self, request, context):
        try:
            token = self._token(context)
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupById(id=request.id, token=token)
            logger.debug(f'[{UserGroupAppServiceListener.userGroupById.__qualname__}] - response: {userGroup}')
            response = UserGroupAppService_userGroupByIdResponse()
            response.userGroup.id = userGroup.id()
            response.userGroup.name = userGroup.name()
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return UserGroupAppService_userGroupByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return UserGroupAppService_userGroupByIdResponse()

    @debugLogger
    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''
