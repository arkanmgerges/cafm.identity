"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository


def test_create_userGroup_object_when_userGroup_already_exist():
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    repo.userGroupByName = Mock(side_effect=UserGroupAlreadyExistException)
    appService = UserGroupApplicationService(repo)
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createObjectOnly(name=name)


def test_create_userGroup_object_when_userGroup_does_not_exist():
    from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    name = 'me'

    repo.userGroupByName = Mock(side_effect=UserGroupDoesNotExistException)
    appService = UserGroupApplicationService(repo)
    userGroup = appService.createObjectOnly(name=name)
    assert isinstance(userGroup, UserGroup)
    assert userGroup.name() == name


def test_create_userGroup_with_event_publishing_when_userGroup_does_not_exist():
    from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    id = '1234567'
    name = 'me'

    repo.userGroupByName = Mock(side_effect=UserGroupDoesNotExistException)
    repo.createUserGroup = Mock(spec=UserGroupRepository.createUserGroup)
    appService = UserGroupApplicationService(repo)
    appService.createUserGroup(id=id, name=name)

    repo.userGroupByName.assert_called_once()
    repo.createUserGroup.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_userGroup_by_name_when_userGroup_exists():
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)

    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo)
    appService.userGroupByName(name=name)

    repo.userGroupByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_userGroup_exists():
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)

    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo)
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createObjectOnly(name=name)


def test_create_userGroup_raise_exception_when_userGroup_exists():
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)

    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo)
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createUserGroup(id='1', name=name)
