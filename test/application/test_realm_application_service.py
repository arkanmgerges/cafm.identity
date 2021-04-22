"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RealmApplicationService import RealmApplicationService
from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.realm.RealmService import RealmService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository

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


def test_create_realm_object_when_realm_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RealmDoesNotExistException import (
        RealmDoesNotExistException,
    )

    DomainPublishedEvents.cleanup()
    repo = Mock(spec=RealmRepository)
    name = "me"
    repo.realmByName = Mock(side_effect=RealmDoesNotExistException)
    realmService = RealmService(realmRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RealmApplicationService(repo, authzService, realmService)
    # Act
    realm = appService.createRealm(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(realm, Realm)
    assert realm.name() == name


def test_get_realm_by_name_when_realm_exists():
    # Arrange
    repo = Mock(spec=RealmRepository)
    name = "me"
    realm = Realm(name=name)
    repo.realmByName = Mock(return_value=realm)
    realmService = RealmService(realmRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RealmApplicationService(repo, authzService, realmService)
    # Act
    appService.realmByName(name=name, token=token)
    # Assert
    repo.realmByName.assert_called_once_with(name=name)


def test_get_realm_by_id_when_realm_exists():
    # Arrange
    repo = Mock(spec=RealmRepository)
    name = "me"
    realm = Realm(id="1234", name=name)
    repo.realmById = Mock(return_value=realm)
    realmService = RealmService(realmRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = RealmApplicationService(repo, authzService, realmService)
    # Act
    appService.realmById(id="1234", token=token)
    # Assert
    repo.realmById.assert_called_once_with(id="1234")
