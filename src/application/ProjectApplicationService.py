"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.request_context_data.ResourceTypeContextDataRequest import ResourceTypeContextDataRequest
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.project.ProjectService import ProjectService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.token.TokenService import TokenService


class ProjectApplicationService:
    def __init__(self, projectRepository: ProjectRepository, authzService: AuthorizationService,
                 projectService: ProjectService):
        self._projectRepository = projectRepository
        self._authzService: AuthorizationService = authzService
        self._projectService = projectService

    def createProject(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.CREATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='project'),
                                        tokenData=tokenData)
        return self._projectService.createProject(id=id, name=name, objectOnly=objectOnly, tokenData=tokenData)

    def updateProject(self, id: str, name: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._projectRepository.projectById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.UPDATE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='project'),
                                        resource=resource,
                                        tokenData=tokenData)
        self._projectService.updateProject(oldObject=resource,
                                           newObject=Project.createFrom(id=id, name=name), tokenData=tokenData)

    def deleteProject(self, id: str, token: str = ''):
        tokenData = TokenService.tokenDataFromToken(token=token)
        roleAccessList: List[RoleAccessPermissionData] = self._authzService.roleAccessPermissionsData(
            tokenData=tokenData, includeAccessTree=False)

        resource = self._projectRepository.projectById(id=id)
        self._authzService.verifyAccess(roleAccessPermissionsData=roleAccessList,
                                        requestedPermissionAction=PermissionAction.DELETE,
                                        requestedContextData=ResourceTypeContextDataRequest(resourceType='project'),
                                        resource=resource,
                                        tokenData=tokenData)
        self._projectService.deleteProject(project=resource, tokenData=tokenData)

    def projectByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.PROJECT.value):
            return self._projectRepository.projectByName(name=name)
        else:
            raise UnAuthorizedException()

    def projectById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.PROJECT.value):
            return self._projectRepository.projectById(id=id)
        else:
            raise UnAuthorizedException()

    def projects(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '',
                 order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.PROJECT.value):
            return self._projectRepository.projectsByOwnedRoles(ownedRoles=ownedRoles,
                                                                resultFrom=resultFrom,
                                                                resultSize=resultSize,
                                                                order=order)
        else:
            raise UnAuthorizedException()
