"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainPublishedEvents
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository

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


def test_create_permission_object_when_permission_already_exist():
    # Arrange
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    repo.permissionByName = Mock(side_effect=PermissionAlreadyExistException)
    appService = PermissionApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(name=name, objectOnly=True, token=token)


def test_create_permission_object_when_permission_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    repo.permissionByName = Mock(side_effect=PermissionDoesNotExistException)
    appService = PermissionApplicationService(repo, authzService)
    # Act
    permission = appService.createPermission(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(permission, Permission)
    assert permission.name() == name


def test_create_permission_with_event_publishing_when_permission_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=PermissionRepository)
    id = '1234567'
    name = 'me'
    repo.permissionByName = Mock(side_effect=PermissionDoesNotExistException)
    repo.createPermission = Mock(spec=PermissionRepository.createPermission)
    appService = PermissionApplicationService(repo, authzService)
    # Act
    appService.createPermission(id=id, name=name, token=token)
    # Assert
    repo.permissionByName.assert_called_once()
    repo.createPermission.assert_called_once()
    assert len(DomainPublishedEvents.postponedEvents()) > 0


def test_get_permission_by_name_when_permission_exists():
    # Arrange
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)
    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo, authzService)
    # Act
    appService.permissionByName(name=name, token=token)
    # Assert
    repo.permissionByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_permission_exists():
    # Arrange
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)
    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(name=name, objectOnly=True, token=token)


def test_create_permission_raise_exception_when_permission_exists():
    # Arrange
    from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(name=name)
    repo.permissionByName = Mock(return_value=permission)
    appService = PermissionApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(PermissionAlreadyExistException):
        permission = appService.createPermission(id='1', name=name, token=token)


def test_get_permission_by_id_when_permission_exists():
    # Arrange
    repo = Mock(spec=PermissionRepository)
    name = 'me'
    permission = Permission(id='1234', name=name)
    repo.permissionById = Mock(return_value=permission)
    appService = PermissionApplicationService(repo, authzService)
    # Act
    appService.permissionById(id='1234', token=token)
    # Assert
    repo.permissionById.assert_called_once_with(id='1234')
