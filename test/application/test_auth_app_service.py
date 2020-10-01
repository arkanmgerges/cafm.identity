"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import pytest
from mock import Mock

from src.application.AuthenticationApplicationService import AuthenticationApplicationService
from src.domain_model.AuthenticationRepository import AuthenticationRepository
from src.domain_model.AuthenticationService import AuthenticationService
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException


def test_authenticate_user_when_exist():
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(return_value={'id': '1234', 'name': 'john', 'role': ['admin']})

    authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))
    token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')

    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_user_when_does_not_exist():
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(side_effect=UserDoesNotExistException)

    with pytest.raises(UserDoesNotExistException):
        authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))
        token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')
