"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from authlib.jose import jwt
from mock import Mock

from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.PolicyRepository import PolicyRepository


def test_is_allowed_when_user_has_super_admin_role_in_token():
    # Arrange
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo, policyService=policyService)
    key = os.getenv('CAFM_JWT_SECRET', 'secret')
    header = {'alg': 'HS256'}
    payload = {'id': '1234', 'name': 'john', 'role': ['super_admin']}
    # Act
    token = jwt.encode(header, payload, key).decode('utf-8')
    # Assert
    assert authzService.isAllowed(token=token)


def test_is_allowed_when_user_does_not_have_super_admin_role_in_token():
    # Arrange
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    policyRepoMock = Mock(spec=PolicyRepository)
    policyRepoMock.allTreeByRoleName = Mock(return_value=[])
    policyService = PolicyControllerService(policyRepoMock)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo, policyService=policyService)
    key = os.getenv('CAFM_JWT_SECRET', 'secret')
    header = {'alg': 'HS256'}
    payload = {'id': '1234', 'name': 'john', 'role': ['admin']}
    # Act
    token = jwt.encode(header, payload, key).decode('utf-8')
    # Act
    isAllowed = authzService.isAllowed(token=token)
    # Assert
    assert isAllowed is False
