"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.user_group.UserGroup import UserGroup


class UserGroupUpdated(DomainEvent):
    def __init__(self, oldUserGroup: UserGroup, newUserGroup: UserGroup):
        super().__init__(id=str(uuid4()), name='user_group_updated')
        self._data = {'old': oldUserGroup.toMap(), 'new': newUserGroup.toMap()}