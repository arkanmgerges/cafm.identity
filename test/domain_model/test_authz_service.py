"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from authlib.jose import jwt
from mock import Mock

from src.domain_model.AuthorizationRepository import AuthorizationRepository
from src.domain_model.AuthorizationService import AuthorizationService


def test_is_allowed_when_user_has_super_admin_role_in_token():
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo)

    key = os.getenv('CAFM_JWT_SECRET', 'secret')
    header = {'alg': 'HS256'}
    payload = {'id': '1234', 'name': 'john', 'role': ['super_admin']}
    token = jwt.encode(header, payload, key).decode('utf-8')

    assert authzService.isAllowedByToken(token=token, data='')


def test_is_allowed_when_user_does_not_have_super_admin_role_in_token():
    authzRepo: AuthorizationRepository = Mock(AuthorizationRepository)
    authzRepo.tokenExists = Mock(return_value=True)
    authzService: AuthorizationService = AuthorizationService(authzRepo=authzRepo)

    key = os.getenv('CAFM_JWT_SECRET', 'secret')
    header = {'alg': 'HS256'}
    payload = {'id': '1234', 'name': 'john', 'role': ['admin']}
    token = jwt.encode(header, payload, key).decode('utf-8')

    assert authzService.isAllowedByToken(token=token, data='') is False
