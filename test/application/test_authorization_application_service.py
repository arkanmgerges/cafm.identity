"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from mock import Mock

from src.application.AuthorizationApplicationService import AuthorizationApplicationService
from src.domain_model.AuthenticationRepository import AuthenticationRepository
from src.domain_model.AuthenticationService import AuthenticationService
from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.AuthorizationService import AuthorizationService


def test_authorization_user_is_allowed_using_token_and_has_super_admin_role():
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo)
    authAppService = AuthorizationApplicationService(authzService=authzService)

    payload = {'id': '1234', 'name': 'john', 'role': ['super_admin']}

    authRepo = Mock(spec=AuthenticationRepository)
    authService = AuthenticationService(authRepo=authRepo)
    token = authService.generateToken(payload=payload)

    assert authAppService.isAllowedByToken(token=token, data='') is True

    assert isinstance(token, str)
    assert len(token) > 0

def test_authorization_user_is_not_allowed_using_token_and_empty_role():
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo)
    authAppService = AuthorizationApplicationService(authzService=authzService)

    payload = {'id': '1234', 'name': 'john', 'role': []}

    authRepo = Mock(spec=AuthenticationRepository)
    authService = AuthenticationService(authRepo=authRepo)
    token = authService.generateToken(payload=payload)

    assert authAppService.isAllowedByToken(token=token, data='') is False

    assert isinstance(token, str)
    assert len(token) > 0
