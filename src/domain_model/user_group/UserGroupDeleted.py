"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

import src.domain_model.user_group.UserGroup as UserGroup
from src.domain_model.event.DomainEvent import DomainEvent


class UserGroupDeleted(DomainEvent):
    def __init__(self, userGroup: UserGroup):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.USER_GROUP_DELETED.value)
        self._data = userGroup.toMap()
