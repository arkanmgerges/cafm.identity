"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.decorator import debugLogger


class PermissionService:
    def __init__(self, permissionRepo: PermissionRepository, policyRepo: PolicyRepository):
        self._repo = permissionRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createPermission(self, obj: Permission, objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if obj.id() == '':
                raise PermissionDoesNotExistException()
            self._repo.permissionByName(name=obj.name())
            raise PermissionAlreadyExistException(obj.name())
        except PermissionDoesNotExistException:
            if objectOnly:
                return Permission.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
            else:
                permission = Permission.createFromObject(obj=obj, publishEvent=True)
                self._repo.createPermission(permission=permission, tokenData=tokenData)
                return permission

    @debugLogger
    def deletePermission(self, permission: Permission, tokenData: TokenData = None):
        self._repo.deletePermission(permission, tokenData=tokenData)
        permission.publishDelete()

    @debugLogger
    def updatePermission(self, oldObject: Permission, newObject: Permission, tokenData: TokenData = None):
        self._repo.updatePermission(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
