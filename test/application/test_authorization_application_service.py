"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from mock import Mock

from src.application.AuthorizationApplicationService import AuthorizationApplicationService
from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository


def test_authorization_user_is_allowed_using_token_and_has_super_admin_role():
    # Arrange
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo, policyService=policyService)
    authAppService = AuthorizationApplicationService(authzService=authzService)
    payload = {'id': '1234', 'name': 'john', 'role': ['super_admin']}
    tokenService = TokenService()
    token = tokenService.generateToken(payload=payload)
    # Act
    isAllowed = authAppService.isAllowed(token=token)
    # Assert
    assert isAllowed is True
    assert isinstance(token, str)
    assert len(token) > 0


def test_authorization_user_is_not_allowed_using_token_and_empty_role():
    # Arrange
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo, policyService=policyService)
    authAppService = AuthorizationApplicationService(authzService=authzService)
    payload = {'id': '1234', 'name': 'john', 'role': []}
    tokenService = TokenService()
    token = tokenService.generateToken(payload=payload)
    # Act
    isAllowed = authAppService.isAllowed(token=token)
    # Assert
    assert isAllowed is False
