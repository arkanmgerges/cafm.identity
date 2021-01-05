"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from src.domain_model.authentication.AuthenticationRepository import AuthenticationRepository
from src.domain_model.token.TokenService import TokenService
from src.resource.logging.decorator import debugLogger
import hashlib


class AuthenticationService:
    def __init__(self, authRepo: AuthenticationRepository):
        self._authRepo = authRepo

    @debugLogger
    def authenticateUser(self, email: str, password: str) -> str:
        """Authenticate user and return jwt token

        Args:
            email (str): User email
            password (str): User password

        Return:
            str: Authentication token

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """
        result = self._authRepo.authenticateUserByEmailAndPassword(email=email, password=password)
        payload = {'id': result['id'], 'roles': result['roles'], 'email': result['email']}
        if 'isOneTimePassword' in result and result['isOneTimePassword'] is True:
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.user.UserWithOneTimePasswordLoggedIn import UserWithOneTimePasswordLoggedIn
            DomainPublishedEvents.addEventForPublishing(UserWithOneTimePasswordLoggedIn(result['id']))
        token = TokenService.generateToken(payload=payload)
        ttl = os.getenv('CAFM_IDENTITY_USER_AUTH_TTL_IN_SECONDS', 300)
        self._authRepo.persistToken(token=token, ttl=ttl)
        return token

    @debugLogger
    def isAuthenticated(self, token: str) -> bool:
        """Check if the user is authenticated, by checking if the token exists, and if exists then refresh it

        Args:
            token (str): The token to be checked

        Returns:
            bool: If the token exists and then it's valid then the response is True, and it returns False otherwise
        """
        try:
            exists = self._authRepo.tokenExists(token=token)
            if exists:
                self._authRepo.refreshToken(token=token, ttl=os.getenv('CAFM_IDENTITY_USER_AUTH_TTL_IN_SECONDS', 300))
            return exists
        except:
            return False

    @debugLogger
    def logout(self, token: str) -> None:
        """Logout the user

        Args:
            token (str): The token to be used for logging out the user
        """
        exists = self._authRepo.tokenExists(token=token)
        if exists:
            self._authRepo.deleteToken(token=token)

    def hashPassword(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()