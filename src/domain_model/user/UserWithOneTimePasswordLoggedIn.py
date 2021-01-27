"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserWithOneTimePasswordLoggedIn, "User With One Time Password Logged In", "event", "message")
"""
class UserWithOneTimePasswordLoggedIn(DomainEvent):
    def __init__(self, id: str):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.USER_WITH_ONE_TIME_PASSWORD_LOGGED_IN.value)
        self._data = {'user_id': id}
