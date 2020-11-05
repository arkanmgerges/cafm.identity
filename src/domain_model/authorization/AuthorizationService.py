"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

import authlib

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.permission.Permission import PermissionAction, Permission
from src.domain_model.policy.PermissionWithResourceTypes import PermissionWithResourceTypes
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant, ResourceType
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.logger import logger


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository, policyService: PolicyControllerService):
        self._authzRepo = authzRepo
        self._policyService = policyService

    def isAllowed(self, token: str, action: str = '', resourceType: str = '', resourceId: str = None) -> bool:
        """Authenticate user and return jwt token

        Args:
            token (str): Token that is used for authorization check
            action (str): An action that can be applied over the resource or/and resource type
            resourceType (str): The type of the resource that the action will be applied to
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
                     resourceTypeConstant: ResourceTypeConstant,
                     tokenData: TokenData):

        if not self._isSuperAdmin(tokenData=tokenData):
            if permissionAction in [PermissionAction.WRITE]:
                if not self._verifyActionByPermissionWithResourceType(permissionAction=permissionAction,
                                                                      resourceTypeConstant=resourceTypeConstant,
                                                                      roleAccessPermissionsData=roleAccessPermissionsData):
                    raise UnAuthorizedException()

    def _isSuperAdmin(self, tokenData) -> bool:
        for role in tokenData.roles():
            if role['name'] == 'super_admin':
                return True
        return False

    def _verifyActionByPermissionWithResourceType(self, permissionAction, resourceTypeConstant,
                                                  roleAccessPermissionsData: List[RoleAccessPermissionData]) -> bool:
        for item in roleAccessPermissionsData:
            permissionsWithResourceTypes: List[PermissionWithResourceTypes] = item.permissions
            for permissionWithResourceTypes in permissionsWithResourceTypes:
                # If we find a permission with the 'action' for 'resource type' then return true
                permission: Permission = permissionWithResourceTypes.permission
                resourceTypes: List[ResourceType] = permissionWithResourceTypes.resourceTypes
                if permissionAction.value in permission.allowedActions():
                    for resourceType in resourceTypes:
                        if resourceTypeConstant.value == resourceType.name():
                            return True
        # We did not find action with resource type, then return false
        return False
