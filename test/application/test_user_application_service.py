"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.UserApplicationService import UserApplicationService
from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.user.User import User
from src.domainmodel.user.UserRepository import UserRepository


def test_create_user_object_when_user_already_exist():
    from src.domainmodel.resource.exception.UserAlreadyExistException import UserAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserRepository)
    username = 'me'
    repo.userByUsername = Mock(side_effect=UserAlreadyExistException)
    appService = UserApplicationService(repo)
    with pytest.raises(UserAlreadyExistException):
        user = appService.createObjectOnly(username=username, password='1234')


def test_create_user_object_when_user_does_not_exist():
    from src.domainmodel.resource.exception.UserDoesNotExistException import UserDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserRepository)
    username = 'me'

    repo.userByUsername = Mock(side_effect=UserDoesNotExistException)
    appService = UserApplicationService(repo)
    user = appService.createObjectOnly(username=username, password='1234')
    assert isinstance(user, User)
    assert user.username() == username


def test_create_user_with_event_publishing_when_user_does_not_exist():
    from src.domainmodel.resource.exception.UserDoesNotExistException import UserDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserRepository)
    id = '1234567'
    username = 'me'
    password = 'pass'

    repo.userByUsername = Mock(side_effect=UserDoesNotExistException)
    repo.createUser = Mock(spec=UserRepository.createUser)
    appService = UserApplicationService(repo)
    appService.createUser(id=id, username=username, password=password)

    repo.userByUsername.assert_called_once()
    repo.createUser.assert_called_once()
