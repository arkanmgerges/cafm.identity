"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.user.User import User


class UserCreated(DomainEvent):
    def __init__(self, user: User):
        super().__init__()
        self._data = json.dumps(user.toMap())

