"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domainmodel.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domainmodel.usergroup.UserGroup import UserGroup


class UserGroupAppServiceListener(identity_pb2_grpc.UserGroupAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def userGroupByName(self, request, context):
        try:
            userGroupAppService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
            userGroup: UserGroup = userGroupAppService.userGroupByName(name=request.name)
            return identity_pb2.UserGroupAppService_userGroupByNameResponse(id=userGroup.id(), name=userGroup.name())
        except UserGroupDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('UserGroup does not exist')
            return identity_pb2.UserGroupAppService_userGroupByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.UserGroupResponse()
