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
        except ProjectDoesNotExistException:
            if objectOnly:
                return Project.createFrom(name=name)
            else:
                project = Project.createFrom(id=id, name=name, publishEvent=True)
                self._projectRepository.createProject(project)
                return project

    def projectByName(self, name: str):
        return self._projectRepository.projectByName(name=name)

    def projectById(self, id: str):
        return self._projectRepository.projectById(id=id)

    def projects(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Project]:
        return self._projectRepository.projectsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom,
                                                            resultSize=resultSize)
