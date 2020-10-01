"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.AuthenticationService import AuthenticationService


class AuthenticationApplicationService:
    def __init__(self, authService: AuthenticationService):
        self._authService: AuthenticationService = authService

    def authenticateUserByNameAndPassword(self, name: str, password: str) -> str:
        """Authenticate user and return token in bytes

        Args:
            name (str): User name
            password (str): User password

        Returns:
            str: User token

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """
        return self._authService.authenticateUser(name=name, password=password)