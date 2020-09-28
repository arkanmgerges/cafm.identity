"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RoleApplicationService import RoleApplicationService
from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.role.Role import Role
from src.domainmodel.role.RoleRepository import RoleRepository


def test_create_role_object_when_role_already_exist():
    from src.domainmodel.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    name = 'me'
    repo.roleByName = Mock(side_effect=RoleAlreadyExistException)
    appService = RoleApplicationService(repo)
    with pytest.raises(RoleAlreadyExistException):
        role = appService.createObjectOnly(name=name)


def test_create_role_object_when_role_does_not_exist():
    from src.domainmodel.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    name = 'me'

    repo.roleByName = Mock(side_effect=RoleDoesNotExistException)
    appService = RoleApplicationService(repo)
    role = appService.createObjectOnly(name=name)
    assert isinstance(role, Role)
    assert role.name() == name


def test_create_role_with_event_publishing_when_role_does_not_exist():
    from src.domainmodel.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    id = '1234567'
    name = 'me'

    repo.roleByName = Mock(side_effect=RoleDoesNotExistException)
    repo.createRole = Mock(spec=RoleRepository.createRole)
    appService = RoleApplicationService(repo)
    appService.createRole(id=id, name=name)

    repo.roleByName.assert_called_once()
    repo.createRole.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_role_by_name_when_role_exists():
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(name=name)

    repo.roleByName = Mock(return_value=role)
    appService = RoleApplicationService(repo)
    appService.roleByName(name=name)

    repo.roleByName.assert_called_once_with(name=name)
