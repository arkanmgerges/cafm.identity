"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum

from src.domain_model.token.TokenData import TokenData
from src.domain_model.token.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.NotAllowedAccessAssignmentException import NotAllowedAccessAssignmentException
from src.domain_model.resource.exception.NotAllowedAssignmentException import NotAllowedAssignmentException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.role.Role import Role


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

    def isAllowed(self, token: str, action: str = '', permissionContext: str = '', resourceId: str = None) -> bool:
        claims = TokenService.claimsFromToken(token=token)
        roles = claims['role']
        for role in roles:
            if role['name'] == 'super_admin':
                return True

            tree = self._policyRepo.allTreeByRoleName(role)

        return False

    def provideAccessRoleToResource(self, role: Role, resource: Resource):
        if resource.type() in [PermissionContextConstant.PROJECT.value, PermissionContextConstant.REALM.value,
                               PermissionContextConstant.OU.value]:
            self._policyRepo.provideAccessRoleToResource(role, resource)
        else:
            raise NotAllowedAccessAssignmentException(
                f'role id: {role.id()} resource id: {resource.id()} and permission context: {resource.type()}')

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

    def raiseNotAllowedException(self, resourceSrc, resourceDst):
        raise NotAllowedAssignmentException(
            f'resource source id: {resourceSrc.id()}, resource source type: {resourceSrc.type()}\nresource destination id: {resourceDst.id()}, permission context: {resourceDst.type()}')

    def roleAccessPermissionsData(self, tokenData: TokenData, includeAccessTree: bool = True):
        return self._policyRepo.roleAccessPermissionsData(tokenData=tokenData, includeAccessTree=includeAccessTree)

    def isOwnerOfResource(self, resource: Resource, tokenData: TokenData) -> bool:
        return self._policyRepo.isOwnerOfResource(resource=resource, tokenData=tokenData)