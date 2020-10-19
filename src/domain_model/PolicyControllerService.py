"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum

from src.domain_model.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository


class PolicyActionConstant(Enum):
    READ = 'read'
    WRITE = 'write'
    DELETE = 'delete'
    UPDATE = 'update'
    ASSIGN = 'assign'
    REVOKE = 'revoke'


class PolicyControllerService:
    def __init__(self, policyRepo: PolicyRepository):
        self._tokenService = TokenService()
        self._policyRepo = policyRepo

    def isAllowed(self, token: str, action: str = '', resourceType: str = '', resourceId: str = None) -> bool:
        claims = self._tokenService.claimsFromToken(token=token)
        roles = claims['role']
        for role in roles:
            if role == 'super_admin':
                return True

            tree = self._policyRepo.allTreeByRoleName(role)

        return False
