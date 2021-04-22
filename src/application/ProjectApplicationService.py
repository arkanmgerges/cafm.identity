"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.authorization.RequestedAuthzObject import RequestedAuthzObject
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
)
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import (
    ResourceTypeContextDataRequest,
)
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.project.ProjectService import ProjectService
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger


class ProjectApplicationService:
    def __init__(
        self,
        projectRepository: ProjectRepository,
        authzService: AuthorizationService,
        projectService: ProjectService,
    ):
        self._projectRepository = projectRepository
        self._authzService: AuthorizationService = authzService
        self._projectService = projectService

    @debugLogger
    def newId(self):
        return Project.createFrom().id()

    @debugLogger
    def createProject(
        self, id: str = None, name: str = "", objectOnly: bool = False, token: str = ""
    ):
        obj: Project = self.constructObject(id=id, name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.CREATE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="project"),
            tokenData=tokenData,
        )
        return self._projectService.createProject(
            obj=obj, objectOnly=objectOnly, tokenData=tokenData
        )

    @debugLogger
    def updateProject(self, id: str, name: str, token: str = ""):
        obj: Project = self.constructObject(id=id, name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._projectRepository.projectById(id=obj.id())
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.UPDATE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="project"),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        self._projectService.updateProject(
            oldObject=resource, newObject=obj, tokenData=tokenData
        )

    @debugLogger
    def deleteProject(self, id: str, token: str = ""):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[
            RoleAccessPermissionData
        ] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False
        )

        resource = self._projectRepository.projectById(id=id)
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessList,
            requestedPermissionAction=PermissionAction.DELETE,
            requestedContextData=ResourceTypeContextDataRequest(resourceType="project"),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        self._projectService.deleteProject(obj=resource, tokenData=tokenData)

    @debugLogger
    def projectByName(self, name: str, token: str = ""):
        resource = self._projectRepository.projectByName(name=name)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.PROJECT.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        return resource

    @debugLogger
    def projectById(self, id: str, token: str = ""):
        resource = self._projectRepository.projectById(id=id)
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        self._authzService.verifyAccess(
            roleAccessPermissionsData=roleAccessPermissionData,
            requestedPermissionAction=PermissionAction.READ,
            requestedContextData=ResourceTypeContextDataRequest(
                resourceType=PermissionContextConstant.PROJECT.value
            ),
            requestedObject=RequestedAuthzObject(obj=resource),
            tokenData=tokenData,
        )
        return resource

    @debugLogger
    def projects(
        self,
        resultFrom: int = 0,
        resultSize: int = 100,
        token: str = "",
        order: List[dict] = None,
    ) -> dict:
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessPermissionData = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData
        )
        return self._projectRepository.projects(
            tokenData=tokenData,
            roleAccessPermissionData=roleAccessPermissionData,
            resultFrom=resultFrom,
            resultSize=resultSize,
            order=order,
        )

    @debugLogger
    def constructObject(self, id: str = None, name: str = "") -> Project:
        return Project.createFrom(id=id, name=name)
