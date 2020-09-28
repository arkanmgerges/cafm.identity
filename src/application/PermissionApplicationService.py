"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
from src.domainmodel.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domainmodel.permission.Permission import Permission
from src.domainmodel.permission.PermissionRepository import PermissionRepository


class PermissionApplicationService:
    def __init__(self, permissionRepository: PermissionRepository):
        self._permissionRepository = permissionRepository

    def createObjectOnly(self, name: str):
        try:
            self._permissionRepository.permissionByName(name=name)
            raise PermissionAlreadyExistException(name=name)
        except PermissionDoesNotExistException:
            return Permission.createFrom(name=name, publishEvent=False)

    def createPermission(self, id: str, name: str):
        try:
            self._permissionRepository.permissionByName(name=name)
            raise PermissionAlreadyExistException(name=name)
        except PermissionDoesNotExistException:
            permission = Permission.createFrom(id=id, name=name)
            self._permissionRepository.createPermission(permission)

    def permissionByName(self, name: str):
        return self._permissionRepository.permissionByName(name=name)
