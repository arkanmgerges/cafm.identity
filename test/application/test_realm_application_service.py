"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.RealmApplicationService import RealmApplicationService
from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.realm.Realm import Realm
from src.domainmodel.realm.RealmRepository import RealmRepository


def test_create_realm_object_when_realm_already_exist():
    from src.domainmodel.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RealmRepository)
    name = 'me'
    repo.realmByRealmname = Mock(side_effect=RealmAlreadyExistException)
    appService = RealmApplicationService(repo)
    with pytest.raises(RealmAlreadyExistException):
        realm = appService.createObjectOnly(name=name)


def test_create_realm_object_when_realm_does_not_exist():
    from src.domainmodel.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RealmRepository)
    name = 'me'

    repo.realmByName = Mock(side_effect=RealmDoesNotExistException)
    appService = RealmApplicationService(repo)
    realm = appService.createObjectOnly(name=name)
    assert isinstance(realm, Realm)
    assert realm.name() == name


def test_create_realm_with_event_publishing_when_realm_does_not_exist():
    from src.domainmodel.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=RealmRepository)
    id = '1234567'
    name = 'me'

    repo.realmByName = Mock(side_effect=RealmDoesNotExistException)
    repo.createRealm = Mock(spec=RealmRepository.createRealm)
    appService = RealmApplicationService(repo)
    appService.createRealm(id=id, name=name)

    repo.realmByName.assert_called_once()
    repo.createRealm.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_realm_by_name_when_realm_exists():
    repo = Mock(spec=RealmRepository)
    name = 'me'
    realm = Realm(name=name)

    repo.realmByName = Mock(return_value=realm)
    appService = RealmApplicationService(repo)
    appService.realmByName(name=name)

    repo.realmByName.assert_called_once_with(name=name)
