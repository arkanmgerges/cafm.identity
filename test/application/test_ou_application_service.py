"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.OuApplicationService import OuApplicationService
from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.ou.OuService import OuService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.token.TokenService import TokenService

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


def test_create_ou_object_when_ou_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.OuDoesNotExistException import (
        OuDoesNotExistException,
    )

    DomainPublishedEvents.cleanup()
    repo = Mock(spec=OuRepository)
    name = "me"
    repo.ouByName = Mock(side_effect=OuDoesNotExistException)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    ou = appService.createOu(id="1234", name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(ou, Ou)
    assert ou.name() == name


def test_get_ou_by_name_when_ou_exists():
    # Arrange
    repo = Mock(spec=OuRepository)
    name = "me"
    ou = Ou(name=name)
    repo.ouByName = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    appService.ouByName(name=name, token=token)
    # Assert
    repo.ouByName.assert_called_once_with(name=name)


def test_get_ou_by_id_when_ou_exists():
    # Arrange
    repo = Mock(spec=OuRepository)
    name = "me"
    ou = Ou(id="1234", name=name)
    repo.ouById = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    appService.ouById(id="1234", token=token)
    # Assert
    repo.ouById.assert_called_once_with(id="1234")
