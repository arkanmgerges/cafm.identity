"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyActionConstant
from src.domain_model.resource.exception.PermissionContextAlreadyExistException import PermissionContextAlreadyExistException
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import PermissionContextDoesNotExistException
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContext, PermissionContextConstant
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository


class PermissionContextApplicationService:
    def __init__(self, permissionContextRepository: PermissionContextRepository, authzService: AuthorizationService):
        self._permissionContextRepository = permissionContextRepository
        self._authzService: AuthorizationService = authzService

    def createPermissionContext(self, id: str = '', type: str = '', objectOnly: bool = False, token: str = ''):
        try:
            if self._authzService.isAllowed(token=token, action=PolicyActionConstant.WRITE.value,
                                            permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
                self._permissionContextRepository.permissionContextByName(type=type)
                raise PermissionContextAlreadyExistException(type)
            else:
                raise UnAuthorizedException()
        except PermissionContextDoesNotExistException:
            if objectOnly:
                return PermissionContext.createFrom(type=type)
            else:
                permissionContext = PermissionContext.createFrom(id=id, type=type, publishEvent=True)
                self._permissionContextRepository.createPermissionContext(permissionContext)
                return permissionContext

    def permissionContextByName(self, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextByName(name=name)
        else:
            raise UnAuthorizedException()

    def permissionContextById(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextById(id=id)
        else:
            raise UnAuthorizedException()

    def permissionContexts(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100, token: str = '', order: List[dict] = None) -> dict:
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.READ.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            return self._permissionContextRepository.permissionContextsByOwnedRoles(ownedRoles=ownedRoles,
                                                                          resultFrom=resultFrom,
                                                                          resultSize=resultSize,
                                                                          order=order)
        else:
            raise UnAuthorizedException()

    def deletePermissionContext(self, id: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.DELETE.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            permissionContext = self._permissionContextRepository.permissionContextById(id=id)
            self._permissionContextRepository.deletePermissionContext(permissionContext)
        else:
            raise UnAuthorizedException()

    def updatePermissionContext(self, id: str, name: str, token: str = ''):
        if self._authzService.isAllowed(token=token, action=PolicyActionConstant.UPDATE.value,
                                        permissionContext=PermissionContextConstant.RESOURCE_TYPE.value):
            permissionContext = self._permissionContextRepository.permissionContextById(id=id)
            permissionContext.update({'name': name})
            self._permissionContextRepository.updatePermissionContext(permissionContext)
        else:
            raise UnAuthorizedException()