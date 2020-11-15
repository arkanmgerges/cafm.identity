"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domain_model.token.TokenData import TokenData


class ProjectService:
    def __init__(self, projectRepo: ProjectRepository, policyRepo: PolicyRepository):
        self._repo = projectRepo
        self._policyRepo = policyRepo

    def createProject(self, id: str = '', name: str = '', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            self._repo.projectByName(name=name)
            raise ProjectAlreadyExistException(name)
        except ProjectDoesNotExistException:
            if objectOnly:
                return Project.createFrom(name=name)
            else:
                project = Project.createFrom(id=id, name=name, publishEvent=True)
                self._repo.createProject(project=project, tokenData=tokenData)
                return project

    def deleteProject(self, project: Project, tokenData: TokenData = None):
        self._repo.deleteProject(project, tokenData=tokenData)
        project.publishDelete()

    def updateProject(self, oldObject: Project, newObject: Project, tokenData: TokenData = None):
        self._repo.updateProject(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
