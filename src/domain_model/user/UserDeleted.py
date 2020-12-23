"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.user.User as User


class UserDeleted(DomainEvent):
    def __init__(self, user: User):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.USER_DELETED.value)
        self._data = user.toMap()
