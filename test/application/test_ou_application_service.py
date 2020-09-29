"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.OuApplicationService import OuApplicationService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository


def test_create_ou_object_when_ou_already_exist():
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=OuRepository)
    name = 'me'
    repo.ouByName = Mock(side_effect=OuAlreadyExistException)
    appService = OuApplicationService(repo)
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createObjectOnly(name=name)


def test_create_ou_object_when_ou_does_not_exist():
    from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=OuRepository)
    name = 'me'

    repo.ouByName = Mock(side_effect=OuDoesNotExistException)
    appService = OuApplicationService(repo)
    ou = appService.createObjectOnly(name=name)
    assert isinstance(ou, Ou)
    assert ou.name() == name


def test_create_ou_with_event_publishing_when_ou_does_not_exist():
    from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=OuRepository)
    id = '1234567'
    name = 'me'

    repo.ouByName = Mock(side_effect=OuDoesNotExistException)
    repo.createOu = Mock(spec=OuRepository.createOu)
    appService = OuApplicationService(repo)
    appService.createOu(id=id, name=name)

    repo.ouByName.assert_called_once()
    repo.createOu.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_ou_by_name_when_ou_exists():
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)

    repo.ouByName = Mock(return_value=ou)
    appService = OuApplicationService(repo)
    appService.ouByName(name=name)

    repo.ouByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_ou_exists():
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)

    repo.ouByName = Mock(return_value=ou)
    appService = OuApplicationService(repo)
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createObjectOnly(name=name)


def test_create_ou_raise_exception_when_ou_exists():
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)

    repo.ouByName = Mock(return_value=ou)
    appService = OuApplicationService(repo)
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createOu(id='1', name=name)
