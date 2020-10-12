"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.PolicyControllerService import PolicyActionConstant
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.resource.exception.PermissionAlreadyExistException import PermissionAlreadyExistException
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant


class PermissionApplicationService:
    def __init__(self, permissionRepository: PermissionRepository, authzService: AuthorizationService):
        self._permissionRepository = permissionRepository
        self._authzService: AuthorizationService = authzService

    def createPermission(self, id: str = '', name: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            resourceType=ResourceTypeConstant.PERMISSION.value):
                self._permissionRepository.permissionByName(name=name)
                raise PermissionAlreadyExistException(name=name)
            else:
                raise UnAuthorizedException()
        except PermissionDoesNotExistException:
            if objectOnly:
                return Permission.createFrom(name=name)
            else:
                permission = Permission.createFrom(id=id, name=name, publishEvent=True)
                self._permissionRepository.createPermission(permission)
                return permission

    def permissionByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PERMISSION.value):
            return self._permissionRepository.permissionByName(name=name)
        else:
            raise UnAuthorizedException()

    def permissionById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PERMISSION.value):
            return self._permissionRepository.permissionById(id=id)
        else:
            raise UnAuthorizedException()

    def permissions(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '') -> List[
        Permission]:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        resourceType=ResourceTypeConstant.PERMISSION.value):
            return self._permissionRepository.permissionsByOwnedRoles(ownedRoles=ownedRoles, resultFrom=resultFrom,
                                                                      resultSize=resultSize)
        else:
            raise UnAuthorizedException()
        
    def deletePermission(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        resourceType=ResourceTypeConstant.PERMISSION.value):
            permission = self._permissionRepository.permissionById(id=id)
            self._permissionRepository.deletePermission(permission)
        else:
            raise UnAuthorizedException()

    def updatePermission(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        resourceType=ResourceTypeConstant.PERMISSION.value):
            permission = self._permissionRepository.permissionById(id=id)
            permission.update({'name': name})
            self._permissionRepository.updatePermission(permission)
        else:
            raise UnAuthorizedException()
