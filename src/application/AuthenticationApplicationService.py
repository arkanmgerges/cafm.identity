"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.authentication.AuthenticationService import AuthenticationService
from src.resource.logging.logger import logger


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

    def isAuthenticated(self, token: str) -> bool:
        logger.debug(f'[{AuthenticationApplicationService.isAuthenticated.__qualname__}] - Received token: {token}')
        return self._authService.isAuthenticated(token=token)

    def logout(self, token: str) -> None:
        logger.debug(f'[{AuthenticationApplicationService.logout.__qualname__}] - Received token: {token}')
        self._authService.logout(token=token)