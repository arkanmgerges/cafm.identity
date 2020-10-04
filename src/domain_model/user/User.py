"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.resource.logging.logger import logger


class User:
    def __init__(self, id: str = str(uuid4()), name='', password=''):
        self._id = id
        self._name = name
        self._password = password

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', password='', publishEvent: bool = False):
        logger.debug(f'[{User.createFrom.__qualname__}] - with name {name}')
        user = User(id, name, password)
        if publishEvent:
            logger.debug(f'[{User.createFrom.__qualname__}] - publish UserCreated event')
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.user.UserCreated import UserCreated
            DomainEventPublisher.addEventForPublishing(UserCreated(user))
        return user

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def password(self) -> str:
        return self._password

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
