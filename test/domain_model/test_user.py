"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.user.User import User


def test_create_user():
    # Act
    user = User('1', '2', '3')
    # Assert
    assert isinstance(user, User)


def test_create_user_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    user = User.createFrom(id=id, name='john', password='1234')
    # Assert
    assert isinstance(user, User)
    assert isinstance(user, Resource)
    assert user.id() == id
    assert user.type() == 'user'
    assert user.name() == 'john'
    assert user.password() == '1234'


def test_that_two_objects_with_same_attributes_are_equal():
    # Act
    object1 = User.createFrom('1234', 'test')
    object2 = User.createFrom('1234', 'test')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Act
    object1 = User.createFrom('1234', 'test')
    object2 = User.createFrom('1234', 'test2')
    # Assert
    assert object1 != object2
