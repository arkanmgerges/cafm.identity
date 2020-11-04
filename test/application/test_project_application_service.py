"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository

token = ''
authzService = None


def setup_function():
    global token
    global authzService
    token = TokenService.generateToken({'role': ['super_admin']})

    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_project_object_when_project_already_exist():
    # Arrange
    from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    repo.projectByProjectName = Mock(side_effect=ProjectAlreadyExistException)
    appService = ProjectApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ProjectAlreadyExistException):
        project = appService.createProject(name=name, objectOnly=True, token=token)


def test_create_project_object_when_project_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    repo.projectByName = Mock(side_effect=ProjectDoesNotExistException)
    appService = ProjectApplicationService(repo, authzService)
    # Act
    project = appService.createProject(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(project, Project)
    assert project.name() == name


def test_create_project_with_event_publishing_when_project_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    id = '1234567'
    name = 'me'
    repo.projectByName = Mock(side_effect=ProjectDoesNotExistException)
    repo.createProject = Mock(spec=ProjectRepository.createProject)
    appService = ProjectApplicationService(repo, authzService)
    # Act
    appService.createProject(id=id, name=name, token=token)
    # Assert
    repo.projectByName.assert_called_once()
    repo.createProject.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_project_by_name_when_project_exists():
    # Arrange
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    project = Project(name=name)
    repo.projectByName = Mock(return_value=project)
    appService = ProjectApplicationService(repo, authzService)
    # Act
    appService.projectByName(name=name, token=token)
    # Assert
    repo.projectByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_role_exists():
    # Arrange
    from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    role = Project(name=name)
    repo.roleByName = Mock(return_value=role)
    appService = ProjectApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ProjectAlreadyExistException):
        role = appService.createProject(name=name, objectOnly=True, token=token)


def test_create_role_raise_exception_when_role_exists():
    # Arrange
    from src.domain_model.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    role = Project(name=name)
    repo.roleByName = Mock(return_value=role)
    appService = ProjectApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ProjectAlreadyExistException):
        role = appService.createProject(id='1', name=name, token=token)


def test_get_project_by_id_when_project_exists():
    # Arrange
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    project = Project(id='1234', name=name)
    repo.projectById = Mock(return_value=project)
    appService = ProjectApplicationService(repo, authzService)
    # Act
    appService.projectById(id='1234', token=token)
    # Assert
    repo.projectById.assert_called_once_with(id='1234')
