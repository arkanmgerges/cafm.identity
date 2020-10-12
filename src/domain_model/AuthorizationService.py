"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import authlib
from authlib.jose import jwt

from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.PolicyControllerService import PolicyControllerService
from src.domain_model.TokenService import TokenService
from src.resource.logging.logger import logger


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository, policyService: PolicyControllerService):
        self._authzRepo = authzRepo
        self._policyService = policyService
        self._tokenService = TokenService()

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
            return False

    def claimsFromToken(self, token: str) -> dict:
        """Get claims by decoding and validating the token

        Args:
            token (str): Token that can carry the info about a user

        Returns:
            dict: A dictionary that represents the claims of the token
            e.g. {"id": "1234", "role": ["super_admin", "accountant"], "name": "john"}

        :raises:
            `BadSignatureError <authlib.jose.errors.BadSignatureError>` If the token is invalid
        """
        return self._tokenService.claimsFromToken(token=token)
