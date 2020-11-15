"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.permission_context.PermissionContext import PermissionContext
from src.domain_model.permission_context.PermissionContextRepository import PermissionContextRepository
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.PermissionContextAlreadyExistException import \
    PermissionContextAlreadyExistException
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import \
    PermissionContextDoesNotExistException
from src.domain_model.token.TokenData import TokenData


class PermissionContextService:
    def __init__(self, permissionContextRepo: PermissionContextRepository, policyRepo: PolicyRepository):
        self._repo = permissionContextRepo
        self._policyRepo = policyRepo

    def createPermissionContext(self, id: str = '', data: dict = None, objectOnly: bool = False,
                                tokenData: TokenData = None):
        try:
            self._repo.permissionContextById(id=id)
            raise PermissionContextAlreadyExistException(id)
        except PermissionContextDoesNotExistException:
            if objectOnly:
                return PermissionContext.createFrom(data=data)
            else:
                permissionContext = PermissionContext.createFrom(id=id, data=data, publishEvent=True)
                self._repo.createPermissionContext(permissionContext=permissionContext, tokenData=tokenData)
                return permissionContext

    def deletePermissionContext(self, permissionContext: PermissionContext, tokenData: TokenData = None):
        self._repo.deletePermissionContext(permissionContext, tokenData=tokenData)
        permissionContext.publishDelete()

    def updatePermissionContext(self, oldObject: PermissionContext, newObject: PermissionContext,
                                tokenData: TokenData = None):
        self._repo.updatePermissionContext(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
