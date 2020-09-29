"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User
from src.domain_model.user.UserCreated import UserCreated


def test_event_UserCreated():
    user = User.createFrom('1', 'john', '1234')
    domainEvent = UserCreated(user)
    assert isinstance(domainEvent, DomainEvent)
    assert json.dumps(domainEvent.data()) == json.dumps({"id": user.id(), "username": user.username()})
    assert isinstance(domainEvent.id(), str)
    assert domainEvent.occurredOn() > 0
