"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents


class UserGroup(Resource):
    def __init__(self, id: str = None, name=''):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId, type='user_group')
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        userGroup = UserGroup(id, name)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.user_group.UserGroupCreated import UserGroupCreated
            DomainPublishedEvents.addEventForPublishing(UserGroupCreated(userGroup))
        return userGroup

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
        DomainPublishedEvents.addEventForPublishing(UserGroupDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user_group.UserGroupUpdated import UserGroupUpdated
        DomainPublishedEvents.addEventForPublishing(UserGroupUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, UserGroup):
            raise NotImplementedError(f'other: {other} can not be compared with UserGroup class')
        return self.id() == other.id() and self.name() == other.name()
