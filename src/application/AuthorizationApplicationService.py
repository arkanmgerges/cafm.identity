"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.AuthenticationService import AuthenticationService
from src.domain_model.AuthorizationService import AuthorizationService


class AuthorizationApplicationService:
    def __init__(self, authzService: AuthorizationService):
        self._authzService: AuthorizationService = authzService

    def isAllowedByToken(self, token: str, data: str) -> bool:
        """Check if the token has access to the context provided by data

        Args:
            token (str): Token to be checked for access
            data (str): Context that is used for verification

        Returns:
            bool: True if the token has access or False otherwise
        """
        return self._authzService.isAllowedByToken(token=token, data=data)
