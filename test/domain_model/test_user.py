"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.user.User import User


def test_create_user():
    # Act
    user = User(id='1', email='me@test.me', password='1234')
    # Assert
    assert isinstance(user, User)


def test_create_user_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    user = User.createFrom(id=id, email='me@test.me', password='1234')
    # Assert
    assert isinstance(user, User)
    assert isinstance(user, Resource)
    assert user.id() == id
    assert user.type() == 'user'
    assert user.email() == 'me@test.me'
    assert user.password() == '1234'


def test_that_two_objects_with_same_attributes_are_equal():
    # Act
    object1 = User.createFrom(id='1234', email='me@test.me')
    object2 = User.createFrom(id='1234', email='me@test.me')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Act
    object1 = User.createFrom(id='1234', email='me@test.me')
    object2 = User.createFrom(id='12345', email='me@test2.me')
    # Assert
    assert object1 != object2
