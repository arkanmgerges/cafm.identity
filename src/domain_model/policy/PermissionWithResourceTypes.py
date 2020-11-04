"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.resource_type.ResourceType import ResourceType


class PermissionWithResourceTypes:
    def __init__(self, permission: Permission = None, resourceTypes: List[ResourceType] = None):
        self.permission = permission
        self.resourceTypes = resourceTypes