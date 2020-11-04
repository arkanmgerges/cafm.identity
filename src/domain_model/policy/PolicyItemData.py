"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.resource_type.ResourceType import ResourceType

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class RoleWithPermissionToResourceTypes:
    def __init__(self, role: str, permission: Permission, resourceTypes: List[ResourceType] = None):
        self.role = role
        self.permission = permission
        self.resourceTypes = resourceTypes


class PolicyItemData:
    def __init__(self, rolesWithPermissions: List[RoleWithPermissionToResourceTypes] = None):
        self.rolesWithPermissions = rolesWithPermissions
