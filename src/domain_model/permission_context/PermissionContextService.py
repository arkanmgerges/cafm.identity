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
from src.resource.logging.decorator import debugLogger


class PermissionContextService:
    def __init__(self, permissionContextRepo: PermissionContextRepository, policyRepo: PolicyRepository):
        self._repo = permissionContextRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createPermissionContext(self, obj: PermissionContext, objectOnly: bool = False,
                                tokenData: TokenData = None):
        try:
            if obj.id() == '':
                raise PermissionContextDoesNotExistException()
            self._repo.permissionContextById(id=obj.id())
            raise PermissionContextAlreadyExistException(obj.id())
        except PermissionContextDoesNotExistException:
            if objectOnly:
                return PermissionContext.createFromObject(obj=obj, generateNewId=True) if obj.id() == '' else obj
            else:
                permissionContext = PermissionContext.createFromObject(obj=obj, publishEvent=True)
                self._repo.createPermissionContext(permissionContext=permissionContext, tokenData=tokenData)
                return permissionContext

    @debugLogger
    def deletePermissionContext(self, permissionContext: PermissionContext, tokenData: TokenData = None):
        self._repo.deletePermissionContext(permissionContext, tokenData=tokenData)
        permissionContext.publishDelete()

    @debugLogger
    def updatePermissionContext(self, oldObject: PermissionContext, newObject: PermissionContext,
                                tokenData: TokenData = None):
        self._repo.updatePermissionContext(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
