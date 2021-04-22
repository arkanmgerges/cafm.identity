"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from mock import Mock

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.user.UserCreated import UserCreated


def setup_function():
    DomainPublishedEvents.cleanup()


def test_add_event_to_postponed_list_and_verify_that_it_is_added():
    # Arrange, Act
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "1"}')
    DomainPublishedEvents.addEventForPublishing(userCreatedMock)
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "2"}')
    DomainPublishedEvents.addEventForPublishing(userCreatedMock)
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "3"}')
    DomainPublishedEvents.addEventForPublishing(userCreatedMock)

    # Assert
    i = 0
    for evt in DomainPublishedEvents.postponedEvents():
        assert isinstance(evt, DomainEvent)
        assert json.loads(evt.data())["id"] == str(i + 1)
        assert isinstance(evt, UserCreated)
        i += 1


def test_clean_domain_event():
    # Arrange
    userCreatedMock = Mock(spec=UserCreated)
    userCreatedMock.data = Mock(return_value='{"id": "1"}')
    # Act
    DomainPublishedEvents.addEventForPublishing(userCreatedMock)
    # Assert
    assert len(DomainPublishedEvents.postponedEvents()) == 1
    DomainPublishedEvents.cleanup()
    assert len(DomainPublishedEvents.postponedEvents()) == 0
