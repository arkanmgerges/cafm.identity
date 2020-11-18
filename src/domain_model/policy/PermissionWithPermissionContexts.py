"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.permission_context.PermissionContext import PermissionContext


class PermissionWithPermissionContexts:
    def __init__(self, permission: Permission = None, permissionContexts: List[PermissionContext] = None):
        self.permission: Permission = permission
        self.permissionContexts: List[PermissionContext] = permissionContexts

    def toMap(self):
        return {"permission": self.permission.toMap(), "permission_contexts": [x.toMap() for x in self.permissionContexts]}
