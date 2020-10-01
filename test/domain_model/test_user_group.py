"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.user_group.UserGroup import UserGroup


def setup_function():
    DomainEventPublisher.cleanup()


def test_create_user_group():
    userGroup = UserGroup()
    assert isinstance(userGroup, UserGroup)


def test_create_by_semantic_constructor():
    id = str(uuid4())
    userGroup = UserGroup.createFrom(id=id, publishEvent=True)
    assert isinstance(userGroup, UserGroup)
    assert userGroup.id() == id
    assert DomainEventPublisher.postponedEvents()[0].data()['id'] == id
