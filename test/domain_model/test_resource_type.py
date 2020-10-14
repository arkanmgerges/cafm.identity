"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource_type.ResourceType import ResourceType


def test_create_resourceType():
    # Act
    resourceType = ResourceType('1', '2')
    # Assert
    assert isinstance(resourceType, ResourceType)


def test_create_resourceType_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    resourceType = ResourceType.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(resourceType, ResourceType)
    assert resourceType.id() == id
    assert resourceType.name() == 'Prj1'


def test_that_two_objects_with_same_attributes_are_equal():
    # Arrange
    object1 = ResourceType.createFrom('1234', 'test')
    object2 = ResourceType.createFrom('1234', 'test')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Arrange
    object1 = ResourceType.createFrom('1234', 'test')
    object2 = ResourceType.createFrom('1234', 'test2')
    # Assert
    assert object1 != object2
