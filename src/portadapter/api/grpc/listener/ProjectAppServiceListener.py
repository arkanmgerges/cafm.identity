"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.portadapter.AppDi as AppDi
import src.resource.proto._generated.identity_pb2 as identity_pb2
import src.resource.proto._generated.identity_pb2_grpc as identity_pb2_grpc
from src.application.ProjectApplicationService import ProjectApplicationService
from src.domainmodel.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domainmodel.project.Project import Project


class ProjectAppServiceListener(identity_pb2_grpc.ProjectAppServiceServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def projectByName(self, request, context):
        try:
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectByName(name=request.name)
            return identity_pb2.ProjectAppService_projectByNameResponse(id=project.id(), name=project.name())
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Project does not exist')
            return identity_pb2.ProjectAppService_projectByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ProjectResponse()
