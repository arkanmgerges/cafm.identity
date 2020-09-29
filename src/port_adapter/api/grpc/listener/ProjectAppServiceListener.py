"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.project.Project import Project
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.resource.proto._generated.project_app_service_pb2 import ProjectAppService_projectByNameResponse
from src.resource.proto._generated.project_app_service_pb2_grpc import ProjectAppServiceServicer


class ProjectAppServiceListener(ProjectAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()

    def __str__(self):
        return self.__class__.__name__

    def projectByName(self, request, context):
        try:
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectByName(name=request.name)
            return ProjectAppService_projectByNameResponse(id=project.id(), name=project.name())
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Project does not exist')
            return ProjectAppService_projectByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ProjectResponse()
