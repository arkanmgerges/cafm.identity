"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User
from src.domain_model.user.UserCreated import UserCreated


def test_event_UserCreated():
    # Act
    user = User.createFrom('1', 'john', '1234')
    domainEvent = UserCreated(user)
    # Assert
    assert isinstance(domainEvent, DomainEvent)
    assert json.dumps(domainEvent.data()) == json.dumps({"id": user.id(), "name": user.name()})
    assert isinstance(domainEvent.id(), str)
    assert domainEvent.occurredOn() > 0
