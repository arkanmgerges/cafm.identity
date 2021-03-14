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
    token = TokenService.generateToken({'id': '11223344', 'email': 'user_1@local.test', 'roles': [{'id': '1234', 'name': 'super_admin'}]})

    DomainPublishedEvents.cleanup()
    authzRepoMock = Mock(spec=AuthorizationRepository)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService = AuthorizationService(authzRepoMock, policyService)


def test_create_user_object_when_user_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=UserRepository)
    email = 'me@me.test'
    repo.userByEmail = Mock(side_effect=UserDoesNotExistException)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    user = appService.createUser(email=email, objectOnly=True, token=token)
    # Assert
    assert isinstance(user, User)
    assert user.email() == email


def test_get_user_by_name_and_password_when_user_exists():
    # Arrange
    repo = Mock(spec=UserRepository)
    email = 'me@local.test'
    password = 'pass'
    user = User(email=email, password=password)
    repo.userByEmailAndPassword = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    appService.userByEmailAndPassword(email=email, password=password)
    # Assert
    repo.userByEmailAndPassword.assert_called_once_with(email=email, password=password)


def test_get_user_by_id_when_user_exists():
    # Arrange
    repo = Mock(spec=UserRepository)
    email = 'me@test.me'
    user = User(id='1234', email=email)
    repo.userById = Mock(return_value=user)
    userService = UserService(userRepo=repo, policyRepo=Mock(sepc=PolicyRepository))
    appService = UserApplicationService(repo, authzService, userService)
    # Act
    appService.userById(id='1234', token=token)
    # Assert
    repo.userById.assert_called_once_with(id='1234')
