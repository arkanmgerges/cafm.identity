"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from mock import Mock

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
from src.domainmodel.user.UserCreated import UserCreated


def setup_function():
    DomainEventPublisher.cleanup()


def test_add_event_to_postponed_list_and_verify_that_it_is_added():
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "1"}')
    DomainEventPublisher.addEventForPublishing(userCreatedMock)
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "2"}')
    DomainEventPublisher.addEventForPublishing(userCreatedMock)
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "3"}')
    DomainEventPublisher.addEventForPublishing(userCreatedMock)

    i = 0
    for evt in DomainEventPublisher.postponedEvents():
        assert isinstance(evt, DomainEvent)
        assert json.loads(evt.data())['id'] == str(i + 1)
        assert isinstance(evt, UserCreated)
        i += 1


def test_clean_domain_event():
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "1"}')
    DomainEventPublisher.addEventForPublishing(userCreatedMock)
    assert len(DomainEventPublisher.postponedEvents()) == 1
    DomainEventPublisher.cleanup()
    assert len(DomainEventPublisher.postponedEvents()) == 0
