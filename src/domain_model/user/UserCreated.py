"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User


class UserCreated(DomainEvent):
    def __init__(self, user: User):
        super().__init__(id=str(uuid4()), name='user_created')
        self._data = user.toMap()

