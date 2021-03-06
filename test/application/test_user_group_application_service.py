"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.domain_model.user_group.UserGroupService import UserGroupService

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


def test_create_userGroup_object_when_userGroup_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.UserGroupDoesNotExistException import (
        UserGroupDoesNotExistException,
    )

    DomainPublishedEvents.cleanup()
    repo = Mock(spec=UserGroupRepository)
    name = "me"
    repo.userGroupByName = Mock(side_effect=UserGroupDoesNotExistException)
    userGroupService = UserGroupService(
        userGroupRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = UserGroupApplicationService(repo, authzService, userGroupService)
    # Act
    userGroup = appService.createUserGroup(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(userGroup, UserGroup)
    assert userGroup.name() == name


def test_get_userGroup_by_name_when_userGroup_exists():
    # Arrange
    repo = Mock(spec=UserGroupRepository)
    name = "me"
    userGroup = UserGroup(name=name)
    repo.userGroupByName = Mock(return_value=userGroup)
    userGroupService = UserGroupService(
        userGroupRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = UserGroupApplicationService(repo, authzService, userGroupService)
    # Act
    appService.userGroupByName(name=name, token=token)
    # Assert
    repo.userGroupByName.assert_called_once_with(name=name)


def test_get_userGroup_by_id_when_userGroup_exists():
    # Arrange
    repo = Mock(spec=UserGroupRepository)
    name = "me"
    userGroup = UserGroup(id="1234", name=name)
    repo.userGroupById = Mock(return_value=userGroup)
    userGroupService = UserGroupService(
        userGroupRepo=repo, policyRepo=Mock(sepc=PolicyRepository)
    )
    appService = UserGroupApplicationService(repo, authzService, userGroupService)
    # Act
    appService.userGroupById(id="1234", token=token)
    # Assert
    repo.userGroupById.assert_called_once_with(id="1234")
