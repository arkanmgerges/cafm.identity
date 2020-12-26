"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User
from src.domain_model.user.UserCreated import UserCreated


def test_event_UserCreated():
    # Act
    user = User.createFrom(id='1', email='john@local.me', password='1234',
                           firstName='John', lastName='Doe', addressOne='lorem ipsum dollor',
                           addressTwo='lorem ipsum dollor', postalCode='A312C5',
                           avatarImage='https://text.com/john.jpg')
    domainEvent = UserCreated(user)
    # Assert
    assert isinstance(domainEvent, DomainEvent)
    assert json.dumps(domainEvent.data()) == json.dumps({"id": user.id(), "email": user.email(),
                                                         "first_name": user.firstName(),
                                                         "last_name": user.lastName(), "address_one": user.addressOne(),
                                                         "address_two": user.addressTwo(),
                                                         "postal_code": user.postalCode(),
                                                         "avatar_image": user.avatarImage()})
    assert isinstance(domainEvent.id(), str)
    assert domainEvent.occurredOn() > 0
