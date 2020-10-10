"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository


class PermissionApplicationService:
    def __init__(self, permissionRepository: PermissionRepository):
        self._permissionRepository = permissionRepository

    def createPermission(self, id: str = '', name: str = '', objectOnly: bool = False):
        try:
            self._permissionRepository.permissionByName(name=name)
            raise PermissionAlreadyExistException(name=name)
        except PermissionDoesNotExistException:
            if objectOnly:                
                return Permission.createFrom(name=name)
            else:
                permission = Permission.createFrom(id=id, name=name, publishEvent=True)
                self._permissionRepository.createPermission(permission)
                return permission

    def permissionByName(self, name: str):
        return self._permissionRepository.permissionByName(name=name)

    def permissionById(self, id: str):
        return self._permissionRepository.permissionById(id=id)

    def permissions(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Permission]:
        return self._permissionRepository.permissionsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom, resultSize=resultSize)
