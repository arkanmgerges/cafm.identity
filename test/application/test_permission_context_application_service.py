"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import uuid

import pytest
from mock import Mock

from src.application.PermissionContextApplicationService import (
    PermissionContextApplicationService,
)
from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.permission_context.PermissionContextService import (
    PermissionContextService,
)
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.permission_context.PermissionContextRepository import (
    PermissionContextRepository,
)

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


def test_create_permissionContext_object_when_permissionContext_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.PermissionContextDoesNotExistException import (
        PermissionContextDoesNotExistException,
    )

    DomainPublishedEvents.cleanup()
    repo = Mock(spec=PermissionContextRepository)
    id = "1234567"
    repo.permissionContextById = Mock(
        side_effect=PermissionContextDoesNotExistException
    )
    permissionContextService = PermissionContextService(
        permissionContextRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionContextApplicationService(
        repo, authzService, permissionContextService
    )
    # Act
    permissionContext = appService.createPermissionContext(
        id=id, objectOnly=True, token=token
    )
    # Assert
    assert isinstance(permissionContext, PermissionContext)
    assert permissionContext.id() == id


def test_get_permissionContext_by_name_when_permissionContext_exists():
    # Arrange
    repo = Mock(spec=PermissionContextRepository)
    id = "1234567"
    permissionContext = PermissionContext(id=id)
    repo.permissionContextById = Mock(return_value=permissionContext)
    permissionContextService = PermissionContextService(
        permissionContextRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionContextApplicationService(
        repo, authzService, permissionContextService
    )
    # Act
    appService.permissionContextById(id=id, token=token)
    # Assert
    repo.permissionContextById.assert_called_once_with(id=id)


def test_get_permissionContext_by_id_when_permissionContext_exists():
    # Arrange
    repo = Mock(spec=PermissionContextRepository)
    id = "1234567"
    permissionContext = PermissionContext(id=id)
    repo.permissionContextById = Mock(return_value=permissionContext)
    permissionContextService = PermissionContextService(
        permissionContextRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = PermissionContextApplicationService(
        repo, authzService, permissionContextService
    )
    # Act
    appService.permissionContextById(id=id, token=token)
    # Assert
    repo.permissionContextById.assert_called_once_with(id=id)
