"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.AuthenticationApplicationService import (
    AuthenticationApplicationService,
)
from src.domain_model.authentication.AuthenticationRepository import (
    AuthenticationRepository,
)
from src.domain_model.authentication.AuthenticationService import AuthenticationService
from src.domain_model.resource.exception.UserDoesNotExistException import (
    UserDoesNotExistException,
)


def test_authenticate_user_when_exist():
    # Arrange
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByEmailAndPassword = Mock(
        return_value={
            "id": "1234",
            "email": "john@local.me",
            "roles": [{"id": "5678", "name": "admin"}],
        }
    )
    authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))
    # Act
    token = authAppService.authenticateUserByEmailAndPassword(
        email="john@local.me", password="1234"
    )
    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
    authRepo.persistToken.assert_called()


def test_authenticate_user_when_does_not_exist():
    # Arrange
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByEmailAndPassword = Mock(
        side_effect=UserDoesNotExistException
    )
    # Act, Assert
    with pytest.raises(UserDoesNotExistException):
        authAppService = AuthenticationApplicationService(
            AuthenticationService(authRepo)
        )
        token = authAppService.authenticateUserByEmailAndPassword(
            email="john@local.me", password="1234"
        )
