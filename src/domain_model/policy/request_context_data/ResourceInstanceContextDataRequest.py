"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.request_context_data.ContextDataRequest import (
    ContextDataRequestConstant,
    ContextDataRequest,
)
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.InvalidCastException import (
    InvalidCastException,
)


class ResourceInstanceContextDataRequest(ContextDataRequest):
    def __init__(self, resource: Resource):
        self.resource = resource
        super().__init__(dataType=ContextDataRequestConstant.RESOURCE_INSTANCE)

    @classmethod
    def castFrom(cls, parentObject: ContextDataRequest):
        if hasattr(parentObject, "resource"):
            return ResourceInstanceContextDataRequest(resource=parentObject.resource)
        raise InvalidCastException(
            f"[{ResourceInstanceContextDataRequest.castFrom.__qualname__}] {parentObject} is not of type {ResourceInstanceContextDataRequest.__qualname__}"
        )
