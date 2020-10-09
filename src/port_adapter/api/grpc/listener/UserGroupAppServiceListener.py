"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import List

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.TokenService import TokenService
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.user_group.UserGroup import UserGroup
from src.resource.logging.logger import logger
from src.resource.proto._generated.user_group_app_service_pb2 import UserGroupAppService_userGroupByNameResponse, \
    UserGroupAppService_userGroupsResponse, UserGroupAppService_userGroupByIdResponse
from src.resource.proto._generated.user_group_app_service_pb2_grpc import UserGroupAppServiceServicer


class UserGroupAppServiceListener(UserGroupAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def userGroupByName(self, request, context):
        try:
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupByName(name=request.name)
            response = UserGroupAppService_userGroupByNameResponse()
            response.userGroup.id = userGroup.id()
            response.userGroup.name = userGroup.name()
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return UserGroupAppService_userGroupByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserGroupResponse()

    def userGroups(self, request, context):
        try:
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            ownedRoles = claims['role'] if 'role' in claims else []
            logger.debug(
                f'[{UserGroupAppServiceListener.userGroups.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t ownedRoles {ownedRoles}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}')
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)

            userGroups: List[UserGroup] = userGroupAppService.userGroups(ownedRoles=ownedRoles,
                                                                         resultFrom=request.resultFrom,
                                                                         resultSize=resultSize)
            response = UserGroupAppService_userGroupsResponse()
            for userGroup in userGroups:
                response.userGroups.add(id=userGroup.id(), name=userGroup.name())
            logger.debug(f'[{UserGroupAppServiceListener.userGroups.__qualname__}] - response: {response}')
            return UserGroupAppService_userGroupsResponse(userGroups=response.userGroups)
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No userGroups found')
            return UserGroupAppService_userGroupByNameResponse()

    def userGroupById(self, request, context):
        try:
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupById(id=request.id)
            logger.debug(f'[{UserGroupAppServiceListener.userGroupById.__qualname__}] - response: {userGroup}')
            response = UserGroupAppService_userGroupByIdResponse()
            response.userGroup.id = userGroup.id()
            response.userGroup.name = userGroup.name()
            return response
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return UserGroupAppService_userGroupByIdResponse()
