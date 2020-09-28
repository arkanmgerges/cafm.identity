"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
from src.domainmodel.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domainmodel.project.Project import Project
from src.domainmodel.project.ProjectRepository import ProjectRepository


class ProjectApplicationService:
    def __init__(self, projectRepository: ProjectRepository):
        self._projectRepository = projectRepository

    def createObjectOnly(self, name: str):
        try:
            self._projectRepository.projectByName(name=name)
            raise ProjectAlreadyExistException(name=name)
        except ProjectDoesNotExistException:
            return Project.createFrom(name=name, publishEvent=False)

    def createProject(self, id: str, name: str):
        try:
            self._projectRepository.projectByName(name=name)
            raise ProjectAlreadyExistException(name=name)
        except ProjectDoesNotExistException:
            project = Project.createFrom(id=id, name=name)
            self._projectRepository.createProject(project)

    def projectByName(self, name: str):
        return self._projectRepository.projectByName(name=name)
