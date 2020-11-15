"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.token.TokenService import TokenService
from src.domain_model.event.DomainEventPublisher import DomainPublishedEvents
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.permission_context.PermissionContext import ResourceType
from src.domain_model.permission_context.PermissionContextRepository import ResourceTypeRepository

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


def test_create_resourceType_object_when_resourceType_already_exist():
    # Arrange
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    repo.resourceTypeByName = Mock(side_effect=ResourceTypeAlreadyExistException)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createResourceType(name=name, objectOnly=True, token=token)


def test_create_resourceType_object_when_resourceType_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    repo.resourceTypeByName = Mock(side_effect=ResourceTypeDoesNotExistException)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act
    resourceType = appService.createResourceType(name=name, objectOnly=True, token=token)
    # Assert
    assert isinstance(resourceType, ResourceType)
    assert resourceType.name() == name


def test_create_resourceType_with_event_publishing_when_resourceType_does_not_exist():
    # Arrange
    from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
    DomainPublishedEvents.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    id = '1234567'
    name = 'me'
    repo.resourceTypeByName = Mock(side_effect=ResourceTypeDoesNotExistException)
    repo.createResourceType = Mock(spec=ResourceTypeRepository.createResourceType)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act
    appService.createResourceType(id=id, name=name, token=token)
    # Assert
    repo.resourceTypeByName.assert_called_once()
    repo.createResourceType.assert_called_once()
    assert len(DomainPublishedEvents.postponedEvents()) > 0


def test_get_resourceType_by_name_when_resourceType_exists():
    # Arrange
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)
    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act
    appService.resourceTypeByName(name=name, token=token)
    # Assert
    repo.resourceTypeByName.assert_called_once_with(name=name)


def test_create_object_only_raise_exception_when_resourceType_exists():
    # Arrange
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)
    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createResourceType(name=name, objectOnly=True, token=token)


def test_create_resourceType_raise_exception_when_resourceType_exists():
    # Arrange
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)
    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act, Assert
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createResourceType(id='1', name=name, token=token)


def test_get_resourceType_by_id_when_resourceType_exists():
    # Arrange
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(id='1234', name=name)
    repo.resourceTypeById = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo, authzService)
    # Act
    appService.resourceTypeById(id='1234', token=token)
    # Assert
    repo.resourceTypeById.assert_called_once_with(id='1234')
