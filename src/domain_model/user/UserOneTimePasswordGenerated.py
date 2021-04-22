"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user.User import User

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserOneTimePasswordGenerated, "CommonEventConstant.USER_ONE_TIME_PASSWORD_GENERATED.value", "message", "event")
"""


class UserOneTimePasswordGenerated(DomainEvent):
    def __init__(self, user: User):
        super().__init__(
            id=str(uuid4()),
            name=CommonEventConstant.USER_ONE_TIME_PASSWORD_GENERATED.value,
        )
        self._data = user.toMap()
