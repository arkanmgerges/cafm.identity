"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class User:
    def __init__(self, id: str = str(uuid4()), username='', password=''):
        self._id = id
        self._username = username
        self._password = password

    @classmethod
    def createNew(cls, id: str = str(uuid4()), username='', password=''):
        from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
        from src.domainmodel.user.UserCreated import UserCreated

        user = User(id, username, password)
        DomainEventPublisher.addEventForPublishing(UserCreated(user))
        return user

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), username='', password=''):
        return User(id, username, password)

    def id(self) -> str:
        return self._id

    def username(self) -> str:
        return self._username

    def password(self) -> str:
        return self._password

    def toMap(self) -> dict:
        return {"id": self.id(), "username": self.username()}
