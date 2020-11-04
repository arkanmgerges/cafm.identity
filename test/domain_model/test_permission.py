"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.permission.Permission import Permission


def test_create_permission():
    # Act
    permission = Permission('1', '2')
    # Assert
    assert isinstance(permission, Permission)


def test_create_permission_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    permission = Permission.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(permission, Permission)
    assert isinstance(permission, Resource)
    assert permission.type() == 'permission'
    assert permission.id() == id
    assert permission.name() == 'Prj1'


def test_that_two_objects_with_same_attributes_are_equal():
    # Arrange
    object1 = Permission.createFrom('1234', 'test')
    object2 = Permission.createFrom('1234', 'test')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Arrange
    object1 = Permission.createFrom('1234', 'test')
    object2 = Permission.createFrom('1234', 'test2')
    # Assert
    assert object1 != object2
