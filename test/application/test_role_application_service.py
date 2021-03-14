"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.role.RoleService import RoleService
from src.domain_model.token.TokenService import TokenService

token = ''
authzService = None


def setup_function():
    global token
    global authzService
    token = TokenService.generateToken(
        {'id': '11223344', 'email': 'user_1@local.test', 'roles': [{'id': '1234', 'name': 'super_admin'}]})

    DomainPublishedEvents.cleanup()
    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_role_object_when_role_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=RoleRepository)
    name = 'me'
    repo.roleByName = Mock(side_effect=RoleDoesNotExistException)
    roleService = RoleService(roleRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RoleApplicationService(repo, authzService, roleService)
    # Act
    role = appService.createRole(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(role, Role)
    assert role.name() == name


def test_get_role_by_name_when_role_exists():
    # Arrange
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(name=name)
    repo.roleByName = Mock(return_value=role)
    roleService = RoleService(roleRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RoleApplicationService(repo, authzService, roleService)
    # Act
    appService.roleByName(name=name, token=token)
    # Assert
    repo.roleByName.assert_called_once_with(name=name)


def test_get_role_by_id_when_role_exists():
    # Arrange
    repo = Mock(spec=RoleRepository)
    name = 'me'
    role = Role(id='1234', name=name)
    repo.roleById = Mock(return_value=role)
    roleService = RoleService(roleRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RoleApplicationService(repo, authzService, roleService)
    # Act
    appService.roleById(id='1234', token=token)
    # Assert
    repo.roleById.assert_called_once_with(id='1234')
