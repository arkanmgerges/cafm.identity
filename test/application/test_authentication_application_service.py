"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from mock import Mock

from src.application.AuthenticationApplicationService import AuthenticationApplicationService
from src.domain_model.authentication.AuthenticationRepository import AuthenticationRepository
from src.domain_model.authentication.AuthenticationService import AuthenticationService


def test_authenticate_user_when_exist():
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(return_value={'id': '1234', 'name': 'john', 'role': ['admin']})
    authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))

    token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')

    assert isinstance(token, str)
    assert len(token) > 0
    authRepo.persistToken.assert_called()


def test_logout_user_when_exist():
    authRepo = Mock(spec=AuthenticationRepository)
    authRepo.authenticateUserByNameAndPassword = Mock(return_value={'id': '1234', 'name': 'john', 'role': ['admin']})
    authAppService = AuthenticationApplicationService(AuthenticationService(authRepo))

    token = authAppService.authenticateUserByNameAndPassword(name='john', password='1234')
    authAppService.logout(token=token)

    assert isinstance(token, str)
    assert len(token) > 0
    authRepo.persistToken.assert_called()
    authRepo.deleteToken.assert_called_with(token=token)