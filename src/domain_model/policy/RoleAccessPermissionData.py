"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithPermissionContexts import PermissionWithPermissionContexts
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role


class RoleAccessPermissionData:
    def __init__(self, role: Role = None, permissions: List[PermissionWithPermissionContexts] = None,
                 ownedBy: Resource = None, accessTree: List[AccessNode] = None):
        self.role: Role = role
        self.permissions: List[PermissionWithPermissionContexts] = permissions if permissions is not None else []
        self.ownedBy = ownedBy
        self.accessTree: List[AccessNode] = accessTree
