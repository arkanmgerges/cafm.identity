"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

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
    assert user.id() == id
    assert user.name() == 'john'
    assert user.password() == '1234'
