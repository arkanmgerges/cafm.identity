"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant


class ProjectApplicationService:
    def __init__(self, projectRepository: ProjectRepository, authzService: AuthorizationService):
        self._projectRepository = projectRepository
        self._authzService: AuthorizationService = authzService

    def createProject(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.PROJECT.value):
                self._projectRepository.projectByName(name=name)
                raise ProjectAlreadyExistException(name=name)
            else:
                raise UnAuthorizedException()
        except ProjectDoesNotExistException:
            if objectOnly:
                return Project.createFrom(name=name)
            else:
                project = Project.createFrom(id=id, name=name, publishEvent=True)
                self._projectRepository.createProject(project)
                return project

    def projectByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PROJECT.value):
            return self._projectRepository.projectByName(name=name)
        else:
            raise UnAuthorizedException()

    def projectById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PROJECT.value):
            return self._projectRepository.projectById(id=id)
        else:
            raise UnAuthorizedException()

    def projects(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '', order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PROJECT.value):
            return self._projectRepository.projectsByOwnedRoles(ownedRoles=ownedRoles,
                                                                resultFrom=resultFrom,
                                                                resultSize=resultSize,
                                                                order=order)
        else:
            raise UnAuthorizedException()

    def deleteProject(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.PROJECT.value):
            project = self._projectRepository.projectById(id=id)
            self._projectRepository.deleteProject(project)
        else:
            raise UnAuthorizedException()

    def updateProject(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.PROJECT.value):
            project = self._projectRepository.projectById(id=id)
            project.update({'name': name})
            self._projectRepository.updateProject(project)
        else:
            raise UnAuthorizedException()