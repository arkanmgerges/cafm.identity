"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.usergroup.UserGroup import UserGroup


class UserGroupCreated(DomainEvent):
    def __init__(self, userGroup: UserGroup):
        super().__init__()
        self._data = json.dumps(userGroup.toMap())
