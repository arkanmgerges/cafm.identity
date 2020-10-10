"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository


def test_create_permission_object_when_permission_already_exist():
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    repo.permissionByName = Mock(side_effect=PermissionAlreadyExistException)
    appService = PermissionApplicationService(repo)
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(name=name, objectOnly=True)


def test_create_permission_object_when_permission_does_not_exist():
    from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=PermissionRepository)
    name = 'me'

    repo.permissionByName = Mock(side_effect=PermissionDoesNotExistException)
    appService = PermissionApplicationService(repo)
    permission = appService.createPermission(name=name, objectOnly=True)
    assert isinstance(permission, Permission)
    assert permission.name() == name


def test_create_permission_with_event_publishing_when_permission_does_not_exist():
    from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=PermissionRepository)
    id = '1234567'
    name = 'me'

    repo.permissionByName = Mock(side_effect=PermissionDoesNotExistException)
    repo.createPermission = Mock(spec=PermissionRepository.createPermission)
    appService = PermissionApplicationService(repo)
    appService.createPermission(id=id, name=name)

    repo.permissionByName.assert_called_once()
    repo.createPermission.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_permission_by_name_when_permission_exists():
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)

    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo)
    appService.permissionByName(name=name)

    repo.permissionByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_permission_exists():
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)

    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo)
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(name=name, objectOnly=True)


def test_create_permission_raise_exception_when_permission_exists():
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)

    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo)
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(id='1', name=name)

def test_get_permission_by_id_when_permission_exists():
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(id='1234', name=name)

    repo.permissionById = Mock(return_value=permission)
    appService = PermissionApplicationService(repo)
    appService.permissionById(id='1234')

    repo.permissionById.assert_called_once_with(id='1234')
