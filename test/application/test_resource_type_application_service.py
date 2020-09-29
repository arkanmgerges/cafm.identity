"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository


def test_create_resourceType_object_when_resourceType_already_exist():
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    repo.resourceTypeByName = Mock(side_effect=ResourceTypeAlreadyExistException)
    appService = ResourceTypeApplicationService(repo)
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createObjectOnly(name=name)


def test_create_resourceType_object_when_resourceType_does_not_exist():
    from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'

    repo.resourceTypeByName = Mock(side_effect=ResourceTypeDoesNotExistException)
    appService = ResourceTypeApplicationService(repo)
    resourceType = appService.createObjectOnly(name=name)
    assert isinstance(resourceType, ResourceType)
    assert resourceType.name() == name


def test_create_resourceType_with_event_publishing_when_resourceType_does_not_exist():
    from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
    DomainEventPublisher.cleanup()
    repo = Mock(spec=ResourceTypeRepository)
    id = '1234567'
    name = 'me'

    repo.resourceTypeByName = Mock(side_effect=ResourceTypeDoesNotExistException)
    repo.createResourceType = Mock(spec=ResourceTypeRepository.createResourceType)
    appService = ResourceTypeApplicationService(repo)
    appService.createResourceType(id=id, name=name)

    repo.resourceTypeByName.assert_called_once()
    repo.createResourceType.assert_called_once()
    assert len(DomainEventPublisher.postponedEvents()) > 0


def test_get_resourceType_by_name_when_resourceType_exists():
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)

    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo)
    appService.resourceTypeByName(name=name)

    repo.resourceTypeByName.assert_called_once_with(name=name)

def test_create_object_only_raise_exception_when_resourceType_exists():
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)

    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo)
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createObjectOnly(name=name)

def test_create_resourceType_raise_exception_when_resourceType_exists():
    from src.domain_model.resource.exception.ResourceTypeAlreadyExistException import ResourceTypeAlreadyExistException
    repo = Mock(spec=ResourceTypeRepository)
    name = 'me'
    resourceType = ResourceType(name=name)

    repo.resourceTypeByName = Mock(return_value=resourceType)
    appService = ResourceTypeApplicationService(repo)
    with pytest.raises(ResourceTypeAlreadyExistException):
        resourceType = appService.createResourceType(id='1', name=name)