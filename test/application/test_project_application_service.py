"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.project.ProjectService import ProjectService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository

token = ''
authzService = None


def setup_function():
    global token
    global authzService
    token = TokenService.generateToken({'id': '11223344', 'email': 'user_1@local.test', 'roles': [{'id': '1234', 'name': 'super_admin'}]})

    DomainPublishedEvents.cleanup()
    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_project_object_when_project_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    repo.projectByName = Mock(side_effect=ProjectDoesNotExistException)
    projectService = ProjectService(projectRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = ProjectApplicationService(repo, authzService, projectService)
    # Act
    project = appService.createProject(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(project, Project)
    assert project.name() == name


def test_get_project_by_id_when_project_exists():
    # Arrange
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    project = Project(id='1234', name=name)
    repo.projectById = Mock(return_value=project)
    projectService = ProjectService(projectRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = ProjectApplicationService(repo, authzService, projectService)
    # Act
    appService.projectById(id='1234', token=token)
    # Assert
    repo.projectById.assert_called_once_with(id='1234')
