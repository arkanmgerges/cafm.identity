"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.policy.PermissionWithResourceTypes import PermissionWithResourceTypes
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role


class RoleAccessPermissionData:
    def __init__(self, role: Role = None, permissions: List[PermissionWithResourceTypes] = None,
                 ownedBy: Resource = None):
        self.role: Role = role
        self.permissions = permissions if permissions is not None else []
        self.ownedBy = ownedBy
