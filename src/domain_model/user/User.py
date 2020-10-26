"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy
from uuid import uuid4

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger


class User(Resource):
    def __init__(self, id: str = None, name='', password=''):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type='user')
        self._name = name
        self._password = password

    @classmethod
    def createFrom(cls, id: str = None, name='', password='', publishEvent: bool = False):
        logger.debug(f'[{User.createFrom.__qualname__}] - with name {name}')
        user = User(id, name, password)
        if publishEvent:
            logger.debug(f'[{User.createFrom.__qualname__}] - publish UserCreated event')
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.user.UserCreated import UserCreated
            DomainEventPublisher.addEventForPublishing(UserCreated(user))
        return user

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name and data['name'] is not None:
            updated = True
            self._name = data['name']
        if 'password' in data and data['password'] != self._password and data['password'] is not None:
            updated = True
            self._password = data['password']
        if updated:
            self.publishUpdate(old)

    def password(self) -> str:
        return self._password

    def publishDelete(self):
        from src.domain_model.user.UserDeleted import UserDeleted
        DomainEventPublisher.addEventForPublishing(UserDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.user.UserUpdated import UserUpdated
        DomainEventPublisher.addEventForPublishing(UserUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, User):
            raise NotImplementedError(f'other: {other} can not be compared with User class')
        return self.id() == other.id() and self.name() == other.name()
