"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository

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


def test_create_role_object_when_role_already_exist():
    # Arrange
    from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    name = 'me'
    repo.roleByName = Mock(side_effect=RoleAlreadyExistException)
    appService = RoleApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RoleAlreadyExistException):
        role = appService.createRole(name=name, objectOnly=True, token=token)


def test_create_role_object_when_role_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    name = 'me'
    repo.roleByName = Mock(side_effect=RoleDoesNotExistException)
    appService = RoleApplicationService(repo, authzService)
    # Act
    role = appService.createRole(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(role, Role)
    assert role.name() == name


def test_create_role_with_event_publishing_when_role_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RoleRepository)
    id = '1234567'
    name = 'me'
    repo.roleByName = Mock(side_effect=RoleDoesNotExistException)
    repo.createRole = Mock(spec=RoleRepository.createRole)
    appService = RoleApplicationService(repo, authzService)
    # Act
    appService.createRole(id=id, name=name, token=token)
    # Assert
    repo.roleByName.assert_called_once()
    repo.createRole.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_role_by_name_when_role_exists():
    # Arrange
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(name=name)
    repo.roleByName = Mock(return_value=role)
    appService = RoleApplicationService(repo, authzService)
    # Act
    appService.roleByName(name=name, token=token)
    # Assert
    repo.roleByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_role_exists():
    # Arrange
    from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(name=name)
    repo.roleByName = Mock(return_value=role)
    appService = RoleApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RoleAlreadyExistException):
        role = appService.createRole(name=name, objectOnly=True, token=token)


def test_create_role_raise_exception_when_role_exists():
    # Arrange
    from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(name=name)
    repo.roleByName = Mock(return_value=role)
    appService = RoleApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RoleAlreadyExistException):
        role = appService.createRole(id='1', name=name, token=token)


def test_get_role_by_id_when_role_exists():
    # Arrange
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(id='1234', name=name)
    repo.roleById = Mock(return_value=role)
    appService = RoleApplicationService(repo, authzService)
    # Act
    appService.roleById(id='1234', token=token)
    # Assert
    repo.roleById.assert_called_once_with(id='1234')

# def test_delete_role_and_check_that_event_is_published():
#     # Arrange
#     repo = Mock(spec=RoleRepository)
#     name = 'me'
#     role = Role(id='1234', name=name)
#     repo.roleById = Mock(return_value=role)
#     def func(o): o.publishDelete()
#     repo.deleteRole = func
#     appService = RoleApplicationService(repo, authzService)
#     # Act
#     appService.deleteRole(id='1234', token=token)
#     # Assert
#     repo.roleById.assert_called_once_with(id='1234')