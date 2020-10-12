"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User


class UserUpdated(DomainEvent):
    def __init__(self, oldUser: User, newUser: User):
        super().__init__(id=str(uuid4()), name='user_updated')
        self._data = {'old': oldUser.toMap(), 'new': newUser.toMap()}

