"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.request_context_data.ContextDataRequest import ContextDataRequestConstant, \
    ContextDataRequest


class ResourceInstanceContextDataRequest(ContextDataRequest):
    def __init__(self, resourceType: str):
        self.resourceType = resourceType
        super().__init__(dataType=ContextDataRequestConstant.RESOURCE_INSTANCE)
