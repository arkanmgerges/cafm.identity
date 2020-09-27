"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.user.User import User
from src.domainmodel.user.UserCreated import UserCreated


def test_event_UserCreated():
    user = User.createNew('1', 'john', '1234')
    domainEvent = UserCreated(user)
    assert isinstance(domainEvent, DomainEvent)
    assert domainEvent.data() == json.dumps({"id": user.id(), "username": user.username()})