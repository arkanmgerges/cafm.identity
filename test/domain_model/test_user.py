"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.user.User import User


def test_create_user():
    user = User('1', '2', '3')
    assert isinstance(user, User)

def test_create_user_with_semantic_constructor():
    id = str(uuid4())
    user = User.createFrom(id=id, name='john', password='1234')
    assert isinstance(user, User)
    assert user.id() == id
    assert user.name() == 'john'
    assert user.password() == '1234'
