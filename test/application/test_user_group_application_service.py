"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository

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


def test_create_userGroup_object_when_userGroup_already_exist():
    # Arrange
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    repo.userGroupByName = Mock(side_effect=UserGroupAlreadyExistException)
    appService = UserGroupApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createUserGroup(name=name, objectOnly=True, token=token)


def test_create_userGroup_object_when_userGroup_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    repo.userGroupByName = Mock(side_effect=UserGroupDoesNotExistException)
    appService = UserGroupApplicationService(repo, authzService)
    # Act
    userGroup = appService.createUserGroup(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(userGroup, UserGroup)
    assert userGroup.name() == name


def test_create_userGroup_with_event_publishing_when_userGroup_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=UserGroupRepository)
    id = '1234567'
    name = 'me'
    repo.userGroupByName = Mock(side_effect=UserGroupDoesNotExistException)
    repo.createUserGroup = Mock(spec=UserGroupRepository.createUserGroup)
    appService = UserGroupApplicationService(repo, authzService)
    # Act
    appService.createUserGroup(id=id, name=name, token=token)
    # Assert
    repo.userGroupByName.assert_called_once()
    repo.createUserGroup.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_userGroup_by_name_when_userGroup_exists():
    # Arrange
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)
    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo, authzService)
    # Act
    appService.userGroupByName(name=name, token=token)
    # Assert
    repo.userGroupByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_userGroup_exists():
    # Arrange
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)
    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createUserGroup(name=name, objectOnly=True, token=token)


def test_create_userGroup_raise_exception_when_userGroup_exists():
    # Arrange
    from src.domain_model.resource.exception.UserGroupAlreadyExistException import UserGroupAlreadyExistException
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(name=name)
    repo.userGroupByName = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(UserGroupAlreadyExistException):
        userGroup = appService.createUserGroup(id='1', name=name, token=token)


def test_get_userGroup_by_id_when_userGroup_exists():
    # Arrange
    repo = Mock(spec=UserGroupRepository)
    name = 'me'
    userGroup = UserGroup(id='1234', name=name)
    repo.userGroupById = Mock(return_value=userGroup)
    appService = UserGroupApplicationService(repo, authzService)
    # Act
    appService.userGroupById(id='1234', token=token)
    # Assert
    repo.userGroupById.assert_called_once_with(id='1234')
