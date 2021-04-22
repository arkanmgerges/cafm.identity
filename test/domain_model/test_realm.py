"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.realm.Realm import Realm


def test_create_realm():
    # Act
    realm = Realm("1", "2")
    # Assert
    assert isinstance(realm, Realm)


def test_create_realm_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    realm = Realm.createFrom(id=id, name="ComABC")
    # Assert
    assert isinstance(realm, Realm)
    assert isinstance(realm, Resource)
    assert realm.type() == "realm"
    assert realm.id() == id
    assert realm.name() == "ComABC"


def test_that_two_objects_with_same_attributes_are_equal():
    # Act
    object1 = Realm.createFrom("1234", "test")
    object2 = Realm.createFrom("1234", "test")
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Act
    object1 = Realm.createFrom("1234", "test")
    object2 = Realm.createFrom("1234", "test2")
    # Assert
    assert object1 != object2
