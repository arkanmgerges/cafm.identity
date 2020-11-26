"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.access_node_content.AccessNodeContent import AccessNodeContentTypeConstant, \
    AccessNodeContent
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.InvalidCastException import InvalidCastException


class ResourceInstanceAccessNodeContent(AccessNodeContent):
    def __init__(self, resource: Resource, resourceName: str):
        self.resource: Resource = resource
        self.resourceName: str = resourceName
        super().__init__(dataType=AccessNodeContentTypeConstant.RESOURCE_INSTANCE)

    @classmethod
    def castFrom(cls, parentObject: AccessNodeContent):
        if hasattr(parentObject, 'resource') and hasattr(parentObject, 'resourceName'):
            return ResourceInstanceAccessNodeContent(resource=parentObject.resource,
                                                     resourceName=parentObject.resourceName)
        raise InvalidCastException(
            f'[{ResourceInstanceAccessNodeContent.castFrom.__qualname__}] {parentObject} is not of type {ResourceInstanceAccessNodeContent.__qualname__}')

    def toMap(self) -> dict:
        result = self.resource.toMap()
        result["name"] = self.resourceName
        return result
