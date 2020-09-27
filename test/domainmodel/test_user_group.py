"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.usergroup.UserGroup import UserGroup


def setup_function():
    DomainEventPublisher.cleanup()


def test_create_user_group():
    userGroup = UserGroup()
    assert isinstance(userGroup, UserGroup)


def test_create_by_semantic_constructor():
    id = str(uuid4())
    userGroup = UserGroup.createNew(id=id)
    assert isinstance(userGroup, UserGroup)
    assert userGroup.id() == id
    assert json.loads(DomainEventPublisher.postponedEvents()[0].data())['id'] == id
