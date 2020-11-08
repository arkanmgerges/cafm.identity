"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

import authlib

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.permission.Permission import PermissionAction, Permission
from src.domain_model.policy.PermissionWithPermissionContexts import PermissionWithPermissionContexts
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant, PermissionContext
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.logger import logger


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository, policyService: PolicyControllerService):
        self._authzRepo = authzRepo
        self._policyService = policyService

    def isAllowed(self, token: str, action: str = '', permissionContext: str = '', resourceId: str = None) -> bool:
        """Authenticate user and return jwt token

        Args:
            token (str): Token that is used for authorization check
            action (str): An action that can be applied over the resource or/and permission context
            permissionContext (str): The type of the resource that the action will be applied to
            resourceId (str): The id of the resource that the action will be applied to

        Return:
            bool:
        """
        try:
            if not self._authzRepo.tokenExists(token=token):
                return False

            if not self._policyService.isAllowed(token=token):
                return False

            return True
        except authlib.jose.errors.BadSignatureError as e:
            logger.exception(
                f'[{AuthorizationService.isAllowed.__qualname__}] - exception raised for invalid token with e: {e}')
            return False
        except Exception as e:
            logger.exception(f'[{AuthorizationService.isAllowed.__qualname__}] - exception raised with e: {e}')
            raise e

    def roleAccessPermissionsData(self, tokenData: TokenData):
        return self._policyService.roleAccessPermissionsData(tokenData=tokenData)

    def verifyAccess(self,
                     roleAccessPermissionsData: List[RoleAccessPermissionData],
                     permissionAction: PermissionAction,
                     permissionContextConstant: PermissionContextConstant,
                     tokenData: TokenData):

        if not self._isSuperAdmin(tokenData=tokenData):
            if permissionAction in [PermissionAction.CREATE]:
                if not self._verifyActionByPermissionWithPermissionContext(permissionAction=permissionAction,
                                                                      permissionContextConstant=permissionContextConstant,
                                                                      roleAccessPermissionsData=roleAccessPermissionsData):
                    raise UnAuthorizedException()

    def _isSuperAdmin(self, tokenData) -> bool:
        for role in tokenData.roles():
            if role['name'] == 'super_admin':
                return True
        return False

    def _verifyActionByPermissionWithPermissionContext(self, permissionAction: PermissionAction, permissionContextConstant: PermissionContextConstant,
                                                  roleAccessPermissionsData: List[RoleAccessPermissionData]) -> bool:
        for item in roleAccessPermissionsData:
            permissionsWithPermissionContexts: List[PermissionWithPermissionContexts] = item.permissions
            for permissionWithPermissionContexts in permissionsWithPermissionContexts:
                # If we find a permission with the 'action' for 'permission context' then return true
                permission: Permission = permissionWithPermissionContexts.permission
                permissionContexts: List[PermissionContext] = permissionWithPermissionContexts.permissionContexts
                if permissionAction.value in permission.allowedActions():
                    for permissionContext in permissionContexts:
                        if permissionContextConstant.value == permissionContext.name():
                            return True
        # We did not find action with permission context, then return false
        return False
