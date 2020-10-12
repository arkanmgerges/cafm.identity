"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from uuid import uuid4

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher


class UserGroup:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False):
        userGroup = UserGroup(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.user_group.UserGroupCreated import UserGroupCreated
            DomainEventPublisher.addEventForPublishing(UserGroupCreated(userGroup))
        return userGroup

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.user_group.UserGroupDeleted import UserGroupDeleted
        DomainEventPublisher.addEventForPublishing(UserGroupDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user_group.UserGroupUpdated import UserGroupUpdated
        DomainEventPublisher.addEventForPublishing(UserGroupUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, UserGroup):
            raise NotImplementedError(f'other: {other} is can not be compared with UserGroup class')
        return self.id() == other.id() and self.name() == other.name()
