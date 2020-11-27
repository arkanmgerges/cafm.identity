"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.OuApplicationService import OuApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.ou.OuService import OuService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository

token = ''
authzService = None


def setup_function():
    global token
    global authzService
    token = TokenService.generateToken({'id': '11223344', 'name': 'user_1', 'roles': [{'id': '1234', 'name': 'super_admin'}]})

    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_ou_object_when_ou_already_exist():
    # Arrange
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=OuRepository)
    name = 'me'
    repo.ouByName = Mock(side_effect=OuAlreadyExistException)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))

    appService = OuApplicationService(repo, authzService, ouService)
    # Act, Assert
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createOu(name=name, objectOnly=True, token=token)


def test_create_ou_object_when_ou_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=OuRepository)
    name = 'me'
    repo.ouByName = Mock(side_effect=OuDoesNotExistException)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    ou = appService.createOu(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(ou, Ou)
    assert ou.name() == name


def test_create_ou_with_event_publishing_when_ou_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.OuDoesNotExistException import OuDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=OuRepository)
    id = '1234567'
    name = 'me'
    repo.ouByName = Mock(side_effect=OuDoesNotExistException)
    repo.createOu = Mock(spec=OuRepository.createOu)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    appService.createOu(id=id, name=name, token=token)
    # Assert
    repo.ouByName.assert_called_once()
    repo.createOu.assert_called_once()
    assert len(DomainPublishedEvents.postponedEvents()) > 0


def test_get_ou_by_name_when_ou_exists():
    # Arrange
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)
    repo.ouByName = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    appService.ouByName(name=name, token=token)
    # Assert
    repo.ouByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_ou_exists():
    # Arrange
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)
    repo.ouByName = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act, Assert
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createOu(name=name, objectOnly=True, token=token)


def test_create_ou_raise_exception_when_ou_exists():
    # Arrange
    from src.domain_model.resource.exception.OuAlreadyExistException import OuAlreadyExistException
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(name=name)
    repo.ouByName = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act, Assert
    with pytest.raises(OuAlreadyExistException):
        ou = appService.createOu(id='1', name=name, token=token)


def test_get_ou_by_id_when_ou_exists():
    # Arrange
    repo = Mock(spec=OuRepository)
    name = 'me'
    ou = Ou(id='1234', name=name)
    repo.ouById = Mock(return_value=ou)
    ouService = OuService(ouRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = OuApplicationService(repo, authzService, ouService)
    # Act
    appService.ouById(id='1234', token=token)
    # Assert
    repo.ouById.assert_called_once_with(id='1234')
