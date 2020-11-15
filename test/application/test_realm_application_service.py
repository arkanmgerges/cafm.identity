"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RealmApplicationService import RealmApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository

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


def test_create_realm_object_when_realm_already_exist():
    # Arrange
    from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=RealmRepository)
    name = 'me'
    repo.realmByName = Mock(side_effect=RealmAlreadyExistException)
    appService = RealmApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RealmAlreadyExistException):
        realm = appService.createRealm(name=name, objectOnly=True, token=token)


def test_create_realm_object_when_realm_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=RealmRepository)
    name = 'me'
    repo.realmByName = Mock(side_effect=RealmDoesNotExistException)
    appService = RealmApplicationService(repo, authzService)
    # Act
    realm = appService.createRealm(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(realm, Realm)
    assert realm.name() == name


def test_create_realm_with_event_publishing_when_realm_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=RealmRepository)
    id = '1234567'
    name = 'me'
    repo.realmByName = Mock(side_effect=RealmDoesNotExistException)
    repo.createRealm = Mock(spec=RealmRepository.createRealm)
    appService = RealmApplicationService(repo, authzService)
    # Act
    appService.createRealm(id=id, name=name, token=token)
    # Assert
    repo.realmByName.assert_called_once()
    repo.createRealm.assert_called_once()
    assert len(DomainPublishedEvents.postponedEvents()) > 0


def test_get_realm_by_name_when_realm_exists():
    # Arrange
    repo = Mock(spec=RealmRepository)
    name = 'me'
    realm = Realm(name=name)
    repo.realmByName = Mock(return_value=realm)
    appService = RealmApplicationService(repo, authzService)
    # Act
    appService.realmByName(name=name, token=token)
    # Assert
    repo.realmByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_realm_exists():
    # Arrange
    from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
    repo = Mock(spec=RealmRepository)
    name = 'me'
    realm = Realm(name=name)
    repo.realmByName = Mock(return_value=realm)
    appService = RealmApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RealmAlreadyExistException):
        realm = appService.createRealm(name=name, objectOnly=True, token=token)


def test_create_realm_raise_exception_when_realm_exists():
    # Arrange
    from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
    repo = Mock(spec=RealmRepository)
    name = 'me'
    realm = Realm(name=name)
    repo.realmByName = Mock(return_value=realm)
    appService = RealmApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(RealmAlreadyExistException):
        realm = appService.createRealm(id='1', name=name, token=token)


def test_get_realm_by_id_when_realm_exists():
    # Arrange
    repo = Mock(spec=RealmRepository)
    name = 'me'
    realm = Realm(id='1234', name=name)
    repo.realmById = Mock(return_value=realm)
    appService = RealmApplicationService(repo, authzService)
    # Act
    appService.realmById(id='1234', token=token)
    # Assert
    repo.realmById.assert_called_once_with(id='1234')
