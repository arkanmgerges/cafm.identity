"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from authlib.jose import jwt

from src.domain_model.AuthenticationRepository import AuthenticationRepository


class AuthenticationService:
    def __init__(self, authRepo: AuthenticationRepository):
        self._authRepo = authRepo

    def authenticateUser(self, name: str, password: str) -> str:
        """Authenticate user and return jwt token

        Args:
            name (str): User name
            password (str): User password

        Return:
            str: Authentication token

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """
        result = self._authRepo.authenticateUserByNameAndPassword(name=name, password=password)
        payload = {'id': result['id'], 'role': result['role'], 'name': result['name']}
        token = self.generateToken(payload=payload)
        ttl = os.getenv('CAFM_IDENTITY_USER_AUTH_TTL_IN_SECONDS', 300)
        self._authRepo.persistToken(token=token, ttl=ttl)
        return token

    def generateToken(self, payload: dict) -> str:
        """Generate token by payload

        Args:
            payload (dict): Data that is used to generate the token

        Returns:
            str: Token string
        """
        header = {'alg': 'HS256'}
        key = os.getenv('CAFM_JWT_SECRET', 'secret')
        token = jwt.encode(header, payload, key).decode('utf-8')
        return token

    def isAuthenticated(self, token: str) -> bool:
        """Check if the user is authenticated, by checking if the token exists, and if exists then refresh it

        Args:
            token (str): The token to be checked

        Returns:
            bool: If the token exists and tnen it's valid then the response is True, and it returns False otherwise
        """
        try:
            exists = self._authRepo.tokenExists(token=token)
            if exists:
                self._authRepo.refreshToken(token=token, ttl=os.getenv('CAFM_IDENTITY_USER_AUTH_TTL_IN_SECONDS', 300))
            return exists
        except:
            return False