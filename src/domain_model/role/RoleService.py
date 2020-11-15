"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository

from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.token.TokenData import TokenData


class RoleService:
    def __init__(self, roleRepo: RoleRepository, policyRepo: PolicyRepository):
        self._repo = roleRepo
        self._policyRepo = policyRepo

    def createRole(self, id: str = '', name: str = '', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            self._repo.roleByName(name=name)
            raise RoleAlreadyExistException(name)
        except RoleDoesNotExistException:
            if objectOnly:
                return Role.createFrom(name=name)
            else:
                role = Role.createFrom(id=id, name=name, publishEvent=True)
                self._repo.createRole(role=role, tokenData=tokenData)
                return role

    def deleteRole(self, role: Role, tokenData: TokenData = None):
        self._repo.deleteRole(role, tokenData=tokenData)
        role.publishDelete()

    def updateRole(self, oldObject: Role, newObject: Role, tokenData: TokenData = None):
        self._repo.updateRole(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
