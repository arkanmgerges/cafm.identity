"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.user.User import User
from src.domain_model.user_group.UserGroup import UserGroup

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserToUserGroupAssigned, "CommonEventConstant.USER_TO_USER_GROUP_ASSIGNED.value", "message", "event")
"""


class UserToUserGroupAssigned(DomainEvent):
    def __init__(self, user: User, userGroup: UserGroup):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.USER_TO_USER_GROUP_ASSIGNED.value
        )
        self._data = {"user_id": user.id(), "user_group_id": userGroup.id()}
