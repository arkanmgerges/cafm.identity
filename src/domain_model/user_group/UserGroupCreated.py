"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user_group.UserGroup import UserGroup

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserGroupCreated, "CommonEventConstant.USER_GROUP_CREATED.value", "message", "event")
"""


class UserGroupCreated(DomainEvent):
    def __init__(self, userGroup: UserGroup):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.USER_GROUP_CREATED.value
        )
        self._data = userGroup.toMap()
