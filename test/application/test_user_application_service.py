"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.UserApplicationService import UserApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user.UserService import UserService

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


def test_create_user_object_when_user_already_exist():
    # Arrange
    from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=UserRepository)
    name = 'me'
    repo.userByName = Mock(side_effect=UserAlreadyExistException)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act, Assert
    with pytest.raises(UserAlreadyExistException):
        user = appService.createUser(id='1234', name=name, password='1234', objectOnly=True, token=token)


def test_create_user_object_when_user_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=UserRepository)
    name = 'me'
    repo.userByName = Mock(side_effect=UserDoesNotExistException)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    user = appService.createUser(name=name, password='1234', objectOnly=True, token=token)
    # Assert
    assert isinstance(user, User)
    assert user.name() == name


def test_create_user_with_event_publishing_when_user_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=UserRepository)
    id = '1234567'
    name = 'me'
    password = 'pass'
    repo.userByName = Mock(side_effect=UserDoesNotExistException)
    repo.createUser = Mock(spec=UserRepository.createUser)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    appService.createUser(id=id, name=name, password=password, token=token)
    # Assert
    repo.userByName.assert_called_once()
    repo.createUser.assert_called_once()
    assert len(DomainPublishedEvents.postponedEvents()) > 0


def test_get_user_by_name_and_password_when_user_exists():
    # Arrange
    repo = Mock(spec=UserRepository)
    name = 'me'
    password = 'pass'
    user = User(name=name, password=password)
    repo.userByNameAndPassword = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    appService.userByNameAndPassword(name=name, password=password)
    # Assert
    repo.userByNameAndPassword.assert_called_once_with(name=name, password=password)


def test_create_object_only_raise_exception_when_user_exists():
    # Arrange
    from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
    repo = Mock(spec=UserRepository)
    name = 'me'
    user = User(id='1', name=name, password='1234')
    repo.userByName = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act, Assert
    with pytest.raises(UserAlreadyExistException):
        user = appService.createUser(id='1234', name=name, password='1234', objectOnly=True, token=token)


def test_create_user_raise_exception_when_user_exists():
    # Arrange
    from src.domain_model.resource.exception.UserAlreadyExistException import UserAlreadyExistException
    repo = Mock(spec=UserRepository)
    name = 'me'
    user = User(id='1', name=name, password='1234')
    repo.userByName = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act, Assert
    with pytest.raises(UserAlreadyExistException):
        user = appService.createUser(id='1', name=name, password='1234', token=token)


def test_get_user_by_id_when_user_exists():
    # Arrange
    repo = Mock(spec=UserRepository)
    name = 'me'
    user = User(id='1234', name=name)
    repo.userById = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    appService.userById(id='1234', token=token)
    # Assert
    repo.userById.assert_called_once_with(id='1234')
