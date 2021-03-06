"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.user.User as User

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserPasswordSet, "CommonEventConstant.USER_PASSWORD_SET.value", "message", "event")
"""


class UserPasswordSet(DomainEvent):
    def __init__(self, user: User):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.USER_PASSWORD_SET.value
        )
        self._data = user.toMap()
