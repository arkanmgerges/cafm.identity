"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant


class ResourceInstanceContextDataRequest:
    def __init__(self, resourceType: str):
        self.type = PermissionContextConstant.RESOURCE_INSTANCE
        self.resourceType = resourceType
