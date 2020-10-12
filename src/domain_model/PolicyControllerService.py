"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum

from src.domain_model.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException


class PolicyActionConstant(Enum):
    READ = 'read'
    WRITE = 'write'
    DELETE = 'delete'
    ASSIGN = 'assign'

class PolicyControllerService:
    def __init__(self, policyRepo: PolicyRepository):
        self._tokenService = TokenService()
        self._policyRepo = policyRepo

    def isAllowed(self, token: str, action: str = '', resourceType: str = '', resourceId: str = None):
        claims = self._tokenService.claimsFromToken(token=token)
        roles = claims['role']
        for role in roles:
            if role == 'super_admin':
                return True

            tree = self._policyRepo.allTreeByRoleName(role)

        raise UnAuthorizedException()

