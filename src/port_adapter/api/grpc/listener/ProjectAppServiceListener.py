"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.project.Project import Project
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.logger import logger
from src.resource.proto._generated.project_app_service_pb2 import ProjectAppService_projectByNameResponse, \
    ProjectAppService_projectsResponse, ProjectAppService_projectByIdResponse
from src.resource.proto._generated.project_app_service_pb2_grpc import ProjectAppServiceServicer


class ProjectAppServiceListener(ProjectAppServiceServicer):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    def projectByName(self, request, context):
        try:
            token = self._token(context)
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectByName(name=request.name, token=token)
            response = ProjectAppService_projectByNameResponse()
            response.project.id = project.id()
            response.project.name = project.name()
            return response
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Project does not exist')
            return ProjectAppService_projectByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return ProjectAppService_projectByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ProjectResponse()

    def projects(self, request, context):
        try:
            token = self._token(context)
            metadata = context.invocation_metadata()
            resultSize = request.resultSize if request.resultSize > 0 else 10
            claims = self._tokenService.claimsFromToken(token=metadata[0].value) if 'token' in metadata[0] else None
            logger.debug(
                f'[{ProjectAppServiceListener.projects.__qualname__}] - metadata: {metadata}\n\t claims: {claims}\n\t \
resultFrom: {request.resultFrom}, resultSize: {resultSize}, token: {token}')
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.order]
            result: dict = projectAppService.projects(
                                                      resultFrom=request.resultFrom,
                                                      resultSize=resultSize,
                                                      token=token,
                                                      order=orderData)
            response = ProjectAppService_projectsResponse()
            for project in result['items']:
                response.projects.add(id=project.id(), name=project.name())
            response.itemCount = result['itemCount']
            logger.debug(f'[{ProjectAppServiceListener.projects.__qualname__}] - response: {response}')
            return ProjectAppService_projectsResponse(projects=response.projects, itemCount=response.itemCount)
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No projects found')
            return ProjectAppService_projectByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return ProjectAppService_projectByNameResponse()

    def projectById(self, request, context):
        try:
            token = self._token(context)
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectById(id=request.id, token=token)
            logger.debug(f'[{ProjectAppServiceListener.projectById.__qualname__}] - response: {project}')
            response = ProjectAppService_projectByIdResponse()
            response.project.id = project.id()
            response.project.name = project.name()
            return response
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Project does not exist')
            return ProjectAppService_projectByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('Un Authorized')
            return ProjectAppService_projectByIdResponse()

    def _token(self, context) -> str:
        metadata = context.invocation_metadata()
        if 'token' in metadata[0]:
            return metadata[0].value
        return ''
