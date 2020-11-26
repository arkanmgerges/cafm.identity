"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum


class AccessNodeContentTypeConstant(Enum):
    RESOURCE_INSTANCE = 'resource_instance'
    RESOURCE_TYPE = 'resource_type'


class AccessNodeContent:
    def __init__(self, dataType: AccessNodeContentTypeConstant):
        self.dataType = dataType

    def toMap(self) -> dict:
        # This is implemented by the derived classes
        return {}
