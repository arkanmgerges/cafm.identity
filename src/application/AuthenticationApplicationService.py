"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.authentication.AuthenticationService import AuthenticationService
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class AuthenticationApplicationService:
    def __init__(self, authService: AuthenticationService):
        self._authService: AuthenticationService = authService

    @debugLogger
    def authenticateUserByEmailAndPassword(self, email: str, password: str) -> str:
        """Authenticate user and return token in bytes

        Args:
            email (str): User email
            password (str): User password

        Returns:
            str: User token

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """
        return self._authService.authenticateUser(email=email, password=password)

    @debugLogger
    def isAuthenticated(self, token: str) -> bool:
        logger.debug(
            f"[{AuthenticationApplicationService.isAuthenticated.__qualname__}] - Received token: {token}"
        )
        return self._authService.isAuthenticated(token=token)

    @debugLogger
    def logout(self, token: str) -> None:
        logger.debug(
            f"[{AuthenticationApplicationService.logout.__qualname__}] - Received token: {token}"
        )
        self._authService.logout(token=token)
