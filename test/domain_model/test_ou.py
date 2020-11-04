"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.ou.Ou import Ou


def test_create_ou():
    # Act
    ou = Ou('1', '2')
    # Assert
    assert isinstance(ou, Ou)


def test_create_ou_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    ou = Ou.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(ou, Ou)
    assert isinstance(ou, Resource)
    assert ou.type() == 'ou'
    assert ou.id() == id
    assert ou.name() == 'Prj1'


def test_that_two_objects_with_same_attributes_are_equal():
    # Arrange
    object1 = Ou.createFrom('1234', 'test')
    object2 = Ou.createFrom('1234', 'test')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Arrange
    object1 = Ou.createFrom('1234', 'test')
    object2 = Ou.createFrom('1234', 'test2')
    # Assert
    assert object1 != object2
