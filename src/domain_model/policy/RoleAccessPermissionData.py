"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithPermissionContexts import (
    PermissionWithPermissionContexts,
)
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role


class RoleAccessPermissionData:
    def __init__(
        self,
        role: Role = None,
        permissions: List[PermissionWithPermissionContexts] = None,
        ownedBy: Resource = None,
        ownerOf: List[Resource] = None,
        accessTree: List[AccessNode] = None,
    ):
        self.role: Role = role
        self.permissions: List[PermissionWithPermissionContexts] = (
            permissions if permissions is not None else []
        )
        self.ownedBy: Resource = ownedBy
        self.ownerOf: List[Resource] = ownerOf
        self.accessTree: List[AccessNode] = accessTree

    def toMap(self):
        return {
            "role": self.role.toMap(),
            "permissions": [x.toMap() for x in self.permissions],
            "owned_by": self.ownedBy.toMap() if self.ownedBy is not None else None,
            "owner_of": [x.toMap() for x in self.ownerOf],
            "access_tree": [x.toMap() for x in self.accessTree],
        }

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"
