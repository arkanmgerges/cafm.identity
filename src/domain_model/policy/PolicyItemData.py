"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.permission_context.PermissionContext import PermissionContext

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class RoleWithPermissionToPermissionContexts:
    def __init__(
        self,
        role: str,
        permission: Permission,
        permissionContexts: List[PermissionContext] = None,
    ):
        self.role = role
        self.permission = permission
        self.permissionContexts = permissionContexts


class PolicyItemData:
    def __init__(
        self, rolesWithPermissions: List[RoleWithPermissionToPermissionContexts] = None
    ):
        self.rolesWithPermissions = rolesWithPermissions
