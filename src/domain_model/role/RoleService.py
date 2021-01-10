"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository

from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.RoleAlreadyExistException import RoleAlreadyExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.decorator import debugLogger


class RoleService:
    def __init__(self, roleRepo: RoleRepository, policyRepo: PolicyRepository):
        self._repo = roleRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createRole(self, obj: Role, objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if obj.id() == '':
                raise RoleDoesNotExistException()
            self._repo.roleByName(name=obj.name())
            raise RoleAlreadyExistException(obj.name())
        except RoleDoesNotExistException:
            if objectOnly:
                return Role.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
            else:
                role = Role.createFromObject(obj=obj, publishEvent=True)
                self._repo.createRole(role=role, tokenData=tokenData)
                return role

    @debugLogger
    def deleteRole(self, role: Role, tokenData: TokenData = None):
        self._repo.deleteRole(role, tokenData=tokenData)
        role.publishDelete()

    @debugLogger
    def updateRole(self, oldObject: Role, newObject: Role, tokenData: TokenData = None):
        self._repo.updateRole(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)


