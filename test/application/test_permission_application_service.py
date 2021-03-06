"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.permission.PermissionService import PermissionService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository

token = ""
authzService = None


def setup_function():
    global token
    global authzService
    token = TokenService.generateToken(
        {
            "id": "11223344",
            "email": "user_1@local.test",
            "roles": [{"id": "1234", "name": "super_admin"}],
        }
    )

    DomainPublishedEvents.cleanup()
    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_permission_object_when_permission_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.PermissionDoesNotExistException import (
        PermissionDoesNotExistException,
    )

    DomainPublishedEvents.cleanup()
    repo = Mock(spec=PermissionRepository)
    name = "me"
    repo.permissionByName = Mock(side_effect=PermissionDoesNotExistException)
    permissionService = PermissionService(
        permissionRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionApplicationService(repo, authzService, permissionService)
    # Act
    permission = appService.createPermission(
        id="1234", name=name, objectOnly=True, token=token
    )
    # Assert
    assert isinstance(permission, Permission)
    assert permission.name() == name


def test_get_permission_by_name_when_permission_exists():
    # Arrange
    repo = Mock(spec=PermissionRepository)
    name = "me"
    permission = Permission(name=name)
    repo.permissionByName = Mock(return_value=permission)
    permissionService = PermissionService(
        permissionRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionApplicationService(repo, authzService, permissionService)
    # Act
    appService.permissionByName(name=name, token=token)
    # Assert
    repo.permissionByName.assert_called_once_with(name=name)


def test_get_permission_by_id_when_permission_exists():
    # Arrange
    repo = Mock(spec=PermissionRepository)
    name = "me"
    permission = Permission(id="1234", name=name)
    repo.permissionById = Mock(return_value=permission)
    permissionService = PermissionService(
        permissionRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionApplicationService(repo, authzService, permissionService)
    # Act
    appService.permissionById(id="1234", token=token)
    # Assert
    repo.permissionById.assert_called_once_with(id="1234")
