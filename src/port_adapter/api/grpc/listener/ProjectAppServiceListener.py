"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time
from typing import Any

import grpc

import src.port_adapter.AppDi as AppDi
from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.project.Project import Project
from src.domain_model.resource.exception.ProjectDoesNotExistException import (
    ProjectDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.token.TokenService import TokenService
from src.port_adapter.api.grpc.listener.BaseListener import BaseListener
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger
from src.resource.logging.opentelemetry.OpenTelemetry import OpenTelemetry
from src.resource.proto._generated.identity.project_app_service_pb2 import (
    ProjectAppService_projectByNameResponse,
    ProjectAppService_projectsResponse,
    ProjectAppService_projectByIdResponse,
    ProjectAppService_newIdResponse, ProjectAppService_projectsByRealmIdResponse,
)
from src.resource.proto._generated.identity.project_app_service_pb2_grpc import (
    ProjectAppServiceServicer,
)


class ProjectAppServiceListener(ProjectAppServiceServicer, BaseListener):
    """The listener function implements the rpc call as described in the .proto file"""

    def __init__(self):
        self.counter = 0
        self.last_print_time = time.time()
        self._tokenService = TokenService()

    def __str__(self):
        return self.__class__.__name__

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def new_id(self, request, context):
        try:
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{ProjectAppServiceListener.new_id.__qualname__}] - claims: {claims}\n\t \
                    token: {token}"
            )
            appService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            return ProjectAppService_newIdResponse(id=appService.newId())
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return ProjectAppService_newIdResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def project_by_name(self, request, context):
        try:
            token = self._token(context)
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectByName(name=request.name, token=token)
            response = ProjectAppService_projectByNameResponse()
            self._addObjectToResponse(obj=project, response=response)
            return response
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Project does not exist")
            return ProjectAppService_projectByNameResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return ProjectAppService_projectByNameResponse()
        # except Exception as e:
        #     context.set_code(grpc.StatusCode.UNKNOWN)
        #     context.set_details(f'{e}')
        #     return identity_pb2.ProjectResponse()

    """
    c4model|cb|identity:Component(identity__grpc__ProjectAppServiceListener__projects, "Get projects", "grpc listener", "Get all projects")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def projects(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{ProjectAppServiceListener.projects.__qualname__}] - claims: {claims}\n\t \
resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.orders]
            result: dict = projectAppService.projects(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
            )
            response = ProjectAppService_projectsResponse()
            for project in result["items"]:
                response.projects.add(id=project.id(), name=project.name())
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{ProjectAppServiceListener.projects.__qualname__}] - response: {response}")
            return ProjectAppService_projectsResponse(
                projects=response.projects, total_item_count=response.total_item_count
            )
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No projects found")
            return ProjectAppService_projectsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return ProjectAppService_projectsResponse()

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def projects_by_realm_id(self, request, context):
        try:
            resultSize = request.result_size if request.result_size >= 0 else 10
            token = self._token(context)
            claims = self._tokenService.claimsFromToken(token=token) if "token" != "" else None
            logger.debug(
                f"[{ProjectAppServiceListener.projects_by_realm_id.__qualname__}] - claims: {claims}\n\t \
    resultFrom: {request.result_from}, resultSize: {resultSize}, token: {token}"
            )
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)

            orderData = [{"orderBy": o.orderBy, "direction": o.direction} for o in request.orders]
            result: dict = projectAppService.projectsByRealmId(
                resultFrom=request.result_from,
                resultSize=resultSize,
                token=token,
                order=orderData,
                realmId=request.realm_id,
            )
            response = ProjectAppService_projectsByRealmIdResponse()
            for project in result["items"]:
                response.projects.add(id=project.id(), name=project.name())
            response.total_item_count = result["totalItemCount"]
            logger.debug(f"[{ProjectAppServiceListener.projects_by_realm_id.__qualname__}] - response: {response}")
            return ProjectAppService_projectsResponse(
                projects=response.projects, total_item_count=response.total_item_count
            )
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No projects found")
            return ProjectAppService_projectsResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return ProjectAppService_projectsResponse()

    """
    c4model|cb|identity:Component(identity__grpc__ProjectAppServiceListener__projectById, "Get project by id", "grpc listener", "Get a project by id")
    """

    @debugLogger
    @OpenTelemetry.grpcTraceOTel
    def project_by_id(self, request, context):
        try:
            token = self._token(context)
            projectAppService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
            project: Project = projectAppService.projectById(id=request.id, token=token)
            logger.debug(f"[{ProjectAppServiceListener.project_by_id.__qualname__}] - response: {project}")
            response = ProjectAppService_projectByIdResponse()
            self._addObjectToResponse(obj=project, response=response)
            return response
        except ProjectDoesNotExistException:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Project does not exist")
            return ProjectAppService_projectByIdResponse()
        except UnAuthorizedException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Un Authorized")
            return ProjectAppService_projectByIdResponse()

    @debugLogger
    def _addObjectToResponse(self, obj: Project, response: Any):
        response.project.id = obj.id()
        response.project.name = obj.name()

    @debugLogger
    def _token(self, context) -> str:
        return super()._token(context=context)
