"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.AuthenticationApplicationService import AuthenticationApplicationService
from src.domain_model.authentication.AuthenticationRepository import AuthenticationRepository
from src.domain_model.authentication.AuthenticationService import AuthenticationService
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException


def test_authenticate_user_when_exist():
    # Arrange
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(return_value={'id': '1234', 'name': 'john', 'role': ['admin']})
    authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))
    # Act
    token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')
    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
    authRepo.persistToken.assert_called()


def test_authenticate_user_when_does_not_exist():
    # Arrange
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(side_effect=UserDoesNotExistException)
    # Act, Assert
    with pytest.raises(UserDoesNotExistException):
        authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))
        token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')
