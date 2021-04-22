"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.request_context_data.ContextDataRequest import (
    ContextDataRequestConstant,
    ContextDataRequest,
)
from src.domain_model.resource.exception.InvalidCastException import (
    InvalidCastException,
)


class ResourceTypeContextDataRequest(ContextDataRequest):
    def __init__(self, resourceType: str):
        self.resourceType = resourceType
        super().__init__(dataType=ContextDataRequestConstant.RESOURCE_TYPE)

    @classmethod
    def castFrom(cls, parentObject: ContextDataRequest):
        if hasattr(parentObject, "resourceType"):
            return ResourceTypeContextDataRequest(
                resourceType=parentObject.resourceType
            )
        raise InvalidCastException(
            f"[{ResourceTypeContextDataRequest.castFrom.__qualname__}] {parentObject} is not of type {ResourceTypeContextDataRequest.__qualname__}"
        )
