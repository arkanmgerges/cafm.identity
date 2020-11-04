"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

import authlib

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.permission.Permission import PermissionAction
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource_type.ResourceType import ResourceTypeConstant
from src.domain_model.token.TokenData import TokenData
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
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

    def verifyAccess(self, roleAccessPermissionsData: List[RoleAccessPermissionData], action:PermissionAction, resourceType:ResourceTypeConstant):
        pass