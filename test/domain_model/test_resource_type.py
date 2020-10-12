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
