"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.request_context_data.ContextDataRequest import ContextDataRequestConstant, \
    ContextDataRequest
from src.domain_model.resource.exception.InvalidCastException import InvalidCastException


class PermissionContextDataRequest(ContextDataRequest):
    def __init__(self, type: str):
        self.type = type
        super().__init__(dataType=ContextDataRequestConstant.PERMISSION)

    @classmethod
    def castFrom(cls, parentObject: ContextDataRequest):
        if hasattr(parentObject, 'type'):
            return PermissionContextDataRequest(type=parentObject.type)
        raise InvalidCastException(
            f'[{PermissionContextDataRequest.castFrom.__qualname__}] {parentObject} is not of type {PermissionContextDataRequest.__qualname__}')
