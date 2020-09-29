"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domainmodel.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domainmodel.usergroup.UserGroup import UserGroup
from src.resource.proto._generated.user_group_app_service_pb2 import UserGroupAppService_userGroupByNameResponse
from src.resource.proto._generated.user_group_app_service_pb2_grpc import UserGroupAppServiceServicer


class UserGroupAppServiceListener(UserGroupAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def userGroupByName(self, request, context):
        try:
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupByName(name=request.name)
            return UserGroupAppService_userGroupByNameResponse(id=userGroup.id(), name=userGroup.name())
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return UserGroupAppService_userGroupByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserGroupResponse()
