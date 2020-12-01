"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum
from typing import List

from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.NotAllowedAccessAssignmentException import NotAllowedAccessAssignmentException
from src.domain_model.resource.exception.NotAllowedAssignmentException import NotAllowedAssignmentException
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenData import TokenData
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger


class PolicyActionConstant(Enum):
    READ = 'read'
    WRITE = 'write'
    DELETE = 'delete'
    UPDATE = 'update'
    ASSIGN = 'assign'
    REVOKE = 'revoke'


class PolicyControllerService:
    def __init__(self, policyRepo: PolicyRepository):
        self._policyRepo = policyRepo

    @debugLogger
    def provideAccessRoleToResource(self, role: Role, resource: Resource):
        if resource.type() in [PermissionContextConstant.PROJECT.value, PermissionContextConstant.REALM.value,
                               PermissionContextConstant.OU.value]:
            self._policyRepo.provideAccessRoleToResource(role, resource)
        else:
            raise NotAllowedAccessAssignmentException(
                f'role id: {role.id()} resource id: {resource.id()} and permission context: {resource.type()}')

    @debugLogger
    def assignResourceToResource(self, resourceSrc: Resource, resourceDst: Resource):
        if (resourceSrc.type() in [PermissionContextConstant.REALM.value,
                                   PermissionContextConstant.OU.value]) and (
                resourceDst.type() in [PermissionContextConstant.PROJECT.value, PermissionContextConstant.REALM.value,
                                       PermissionContextConstant.OU.value]):
            if resourceSrc.type() == PermissionContextConstant.OU.value:
                # Not allowed to assign ou to a realm
                if resourceDst.type() == PermissionContextConstant.REALM.value:
                    self.raiseNotAllowedException(resourceSrc, resourceDst)

            self._policyRepo.assignResourceToResource(resourceSrc, resourceDst)
        else:
            self.raiseNotAllowedException(resourceSrc, resourceDst)

    @debugLogger
    def raiseNotAllowedException(self, resourceSrc, resourceDst):
        raise NotAllowedAssignmentException(
            f'resource source id: {resourceSrc.id()}, resource source type: {resourceSrc.type()}\nresource destination id: {resourceDst.id()}, permission context: {resourceDst.type()}')

    @debugLogger
    def roleAccessPermissionsData(self, tokenData: TokenData, includeAccessTree: bool = True):
        return self._policyRepo.roleAccessPermissionsData(tokenData=tokenData, includeAccessTree=includeAccessTree)

    @debugLogger
    def isOwnerOfResource(self, resource: Resource, tokenData: TokenData) -> bool:
        return self._policyRepo.isOwnerOfResource(resource=resource, tokenData=tokenData)

    @debugLogger
    def resourcesOfTypeByTokenData(self, resourceType: str = '', tokenData: TokenData = None,
                                   roleAccessPermissionData: List[RoleAccessPermissionData] = None, sortData: str = ''):
        return self._policyRepo.resourcesOfTypeByTokenData(resourceType, tokenData, roleAccessPermissionData, sortData)

    @debugLogger
    def permissionsByTokenData(self, tokenData: TokenData = None,
                               roleAccessPermissionData: List[RoleAccessPermissionData] = None, sortData: str = ''):
        return self._policyRepo.permissionsByTokenData(tokenData, roleAccessPermissionData, sortData)

    @debugLogger
    def permissionContextsByTokenData(self, tokenData: TokenData = None,
                                      roleAccessPermissionData: List[RoleAccessPermissionData] = None,
                                      sortData: str = ''):
        return self._policyRepo.permissionContextsByTokenData(tokenData, roleAccessPermissionData, sortData)

    @debugLogger
    def rolesTrees(self, tokenData: TokenData = None,
                   roleAccessPermissionData: List[RoleAccessPermissionData] = None) -> List[RoleAccessPermissionData]:
        return self._policyRepo.rolesTrees(tokenData, roleAccessPermissionData)

    @debugLogger
    def roleTree(self, tokenData: TokenData = None, roleId: str = '',
                   roleAccessPermissionData: List[RoleAccessPermissionData] = None) -> RoleAccessPermissionData:
        return self._policyRepo.roleTree(tokenData, roleId, roleAccessPermissionData)