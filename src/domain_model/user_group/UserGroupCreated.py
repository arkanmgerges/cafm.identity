"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user_group.UserGroup import UserGroup


class UserGroupCreated(DomainEvent):
    def __init__(self, userGroup: UserGroup):
        super().__init__(id=str(uuid4()), name='user_group_created')
        self._data = userGroup.toMap()
