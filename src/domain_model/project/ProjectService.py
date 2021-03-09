"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.decorator import debugLogger


class ProjectService:
    def __init__(self, projectRepo: ProjectRepository, policyRepo: PolicyRepository):
        self._repo = projectRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createProject(self, obj: Project, objectOnly: bool = False, tokenData: TokenData = None):
        if objectOnly:
            return Project.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
        else:
            obj = Project.createFromObject(obj=obj, publishEvent=True)
            self._repo.save(obj=obj, tokenData=tokenData)
            return obj

    @debugLogger
    def deleteProject(self, obj: Project, tokenData: TokenData = None):
        obj.publishDelete()
        self._repo.deleteProject(obj=obj, tokenData=tokenData)

    @debugLogger
    def updateProject(self, oldObject: Project, newObject: Project, tokenData: TokenData = None):
        newObject.publishUpdate(oldObject)
        self._repo.save(obj=newObject, tokenData=tokenData)
