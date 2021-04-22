"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role


def test_create_role():
    # Act
    role = Role("1", "2")
    # Assert
    assert isinstance(role, Role)


def test_create_role_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    role = Role.createFrom(id=id, name="Prj1", title="Title")
    # Assert
    assert isinstance(role, Role)
    assert isinstance(role, Resource)
    assert role.type() == "role"
    assert role.id() == id
    assert role.name() == "Prj1"
    assert role.title() == "Title"


def test_that_two_objects_with_same_attributes_are_equal():
    # Act
    object1 = Role.createFrom("1234", "test", "title")
    object2 = Role.createFrom("1234", "test", "title")
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Act
    object1 = Role.createFrom("1234", "test", "title")
    object2 = Role.createFrom("1234", "test2", "title2")
    # Assert
    assert object1 != object2
