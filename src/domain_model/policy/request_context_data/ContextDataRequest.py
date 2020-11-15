"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum


class ContextDataRequestConstant(Enum):
    RESOURCE_INSTANCE = 'resource_instance'
    RESOURCE_TYPE = 'resource_type'


class ContextDataRequest:
    def __init__(self, dataType: ContextDataRequestConstant):
        self.dataType = dataType
