"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainPublishedEvents
from src.domain_model.user_group.UserGroup import UserGroup


def setup_function():
    DomainPublishedEvents.cleanup()


def test_create_user_group():
    # Act
    userGroup = UserGroup()
    # Assert
    assert isinstance(userGroup, UserGroup)
    assert isinstance(userGroup, Resource)
    assert userGroup.type() == 'user_group'


def test_create_by_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    userGroup = UserGroup.createFrom(id=id, publishEvent=True)
    # Assert
    assert isinstance(userGroup, UserGroup)
    assert userGroup.id() == id
    assert DomainPublishedEvents.postponedEvents()[0].data()['id'] == id


def test_that_two_objects_with_same_attributes_are_equal():
    # Arrange
    object1 = UserGroup.createFrom('1234', 'test')
    object2 = UserGroup.createFrom('1234', 'test')
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Arrange
    object1 = UserGroup.createFrom('1234', 'test')
    object2 = UserGroup.createFrom('1234', 'test2')
    # Assert
    assert object1 != object2
