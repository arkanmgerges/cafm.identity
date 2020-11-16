"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum
from typing import Any


class RequestedAuthzObjectEnum(Enum):
    RESOURCE = 'resource'
    PERMISSION = 'permission'
    PERMISSION_CONTEXT = 'permission_context'


class RequestedAuthzObject:
    def __init__(self, objType: RequestedAuthzObjectEnum = RequestedAuthzObjectEnum.RESOURCE, obj: Any = None):
        self.type = objType
        self.obj = obj
