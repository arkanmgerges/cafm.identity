"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import authlib
from authlib.jose import jwt

from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.TokenService import TokenService
from src.resource.logging.logger import logger


class AuthorizationService:
    def __init__(self, authzRepo: AuthorizationRepository):
        self._authzRepo = authzRepo
        self._tokenService = TokenService()

    def isAllowedByToken(self, token: str, data: str) -> bool:
        """Authenticate user and return jwt token

        Args:
            token (str): Token that is used for authorization check
            data (str): Data associated, to determine if the user has allowed to take action on data
            based on this token

        Return:
            bool:
        """
        try:
            if not self._authzRepo.tokenExists(token=token):
                return False
            claims = self.claimsFromToken(token=token)
            if 'role' in claims and 'super_admin' in claims['role']:
                return True
            return False
        except authlib.jose.errors.BadSignatureError as e:
            logger.exception(
                f'[{AuthorizationService.isAllowedByToken.__qualname__}] - exception raised for invalid token with e: {e}')
            return False
        except Exception as e:
            logger.exception(f'[{AuthorizationService.isAllowedByToken.__qualname__}] - exception raised with e: {e}')
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
