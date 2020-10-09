"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository


class ProjectApplicationService:
    def __init__(self, projectRepository: ProjectRepository):
        self._projectRepository = projectRepository

    def createObjectOnly(self, name: str):
        try:
            self._projectRepository.projectByName(name=name)
            raise ProjectAlreadyExistException(name=name)
        except ProjectDoesNotExistException:
            return Project.createFrom(name=name)

    def createProject(self, id: str, name: str):
        try:
            self._projectRepository.projectByName(name=name)
            raise ProjectAlreadyExistException(name=name)
        except ProjectDoesNotExistException:
            project = Project.createFrom(id=id, name=name, publishEvent=True)
            self._projectRepository.createProject(project)
            return project

    def projectByName(self, name: str):
        return self._projectRepository.projectByName(name=name)

    def projectById(self, id: str):
        return self._projectRepository.projectById(id=id)

    def projects(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Project]:
        return self._projectRepository.projectsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
