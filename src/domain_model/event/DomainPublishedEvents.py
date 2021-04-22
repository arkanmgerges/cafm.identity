"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.event.DomainEvent import DomainEvent


class DomainPublishedEvents:
    _postponedEvents = []

    @classmethod
    def addEventForPublishing(cls, domainEvent: DomainEvent) -> None:
        """Add event to the list of postponed events"""
        cls._postponedEvents.append(domainEvent)

    @classmethod
    def postponedEvents(cls) -> List[DomainEvent]:
        """Get list of postponed domain events"""
        return cls._postponedEvents

    @classmethod
    def cleanup(cls) -> None:
        """Empty all the domain events"""
        cls._postponedEvents = []
