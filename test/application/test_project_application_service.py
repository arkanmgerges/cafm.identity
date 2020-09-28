"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.ProjectApplicationService import ProjectApplicationService
from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.project.Project import Project
from src.domainmodel.project.ProjectRepository import ProjectRepository


def test_create_project_object_when_project_already_exist():
    from src.domainmodel.resource.exception.ProjectAlreadyExistException import ProjectAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    repo.projectByProjectName = Mock(side_effect=ProjectAlreadyExistException)
    appService = ProjectApplicationService(repo)
    with pytest.raises(ProjectAlreadyExistException):
        project = appService.createObjectOnly(name=name)


def test_create_project_object_when_project_does_not_exist():
    from src.domainmodel.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    name = 'me'

    repo.projectByName = Mock(side_effect=ProjectDoesNotExistException)
    appService = ProjectApplicationService(repo)
    project = appService.createObjectOnly(name=name)
    assert isinstance(project, Project)
    assert project.name() == name


def test_create_project_with_event_publishing_when_project_does_not_exist():
    from src.domainmodel.resource.exception.ProjectDoesNotExistException import ProjectDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ProjectRepository)
    id = '1234567'
    name = 'me'

    repo.projectByName = Mock(side_effect=ProjectDoesNotExistException)
    repo.createProject = Mock(spec=ProjectRepository.createProject)
    appService = ProjectApplicationService(repo)
    appService.createProject(id=id, name=name)

    repo.projectByName.assert_called_once()
    repo.createProject.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_project_by_name_when_project_exists():
    repo = Mock(spec=ProjectRepository)
    name = 'me'
    project = Project(name=name)

    repo.projectByName = Mock(return_value=project)
    appService = ProjectApplicationService(repo)
    appService.projectByName(name=name)

    repo.projectByName.assert_called_once_with(name=name)
