"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.resource.proto._generated.resource_type_app_service_pb2 import \
    ResourceTypeAppService_resourceTypeByNameResponse
from src.resource.proto._generated.resource_type_app_service_pb2_grpc import ResourceTypeAppServiceServicer


class ResourceTypeAppServiceListener(ResourceTypeAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def resourceTypeByName(self, request, context):
        try:
            resourceTypeAppService: ResourceTypeApplicationService = AppDi.instance.get(ResourceTypeApplicationService)
            resourceType: ResourceType = resourceTypeAppService.resourceTypeByName(name=request.name)
            return ResourceTypeAppService_resourceTypeByNameResponse(id=resourceType.id(), name=resourceType.name())
        except ResourceTypeDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('ResourceType does not exist')
            return ResourceTypeAppService_resourceTypeByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ResourceTypeResponse()
