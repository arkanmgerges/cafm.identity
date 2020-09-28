"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.domainmodel.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domainmodel.resourcetype.ResourceType import ResourceType


class ResourceTypeAppServiceListener(identity_pb2_grpc.ResourceTypeAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def resourceTypeByName(self, request, context):
        try:
            resourceTypeAppService: ResourceTypeApplicationService = AppDi.instance.get(ResourceTypeApplicationService)
            resourceType: ResourceType = resourceTypeAppService.resourceTypeByName(name=request.name)
            return identity_pb2.ResourceTypeAppService_resourceTypeByNameResponse(id=resourceType.id(), name=resourceType.name())
        except ResourceTypeDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('ResourceType does not exist')
            return identity_pb2.ResourceTypeAppService_resourceTypeByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ResourceTypeResponse()
