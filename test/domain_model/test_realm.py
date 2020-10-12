"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.realm.Realm import Realm


def test_create_realm():
    # Act
    realm = Realm('1', '2')
    # Assert
    assert isinstance(realm, Realm)


def test_create_realm_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    realm = Realm.createFrom(id=id, name='ComABC')
    # Assert
    assert isinstance(realm, Realm)
    assert realm.id() == id
    assert realm.name() == 'ComABC'
