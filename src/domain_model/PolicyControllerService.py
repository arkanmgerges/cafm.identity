"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.TokenService import TokenService
from src.domain_model.policy.PolicyRepository import PolicyRepository


class PolicyControllerService:
    def __init__(self, policyRepo: PolicyRepository):
        self._tokenService = TokenService()
        self._policyRepo = policyRepo

    def isAllowed(self, token: str, action: str, resourceType: str, resourceId: str = None):
        claims = self._tokenService.claimsFromToken(token=token)
        roles = claims['role']
        for role in roles:
            if role == 'super_admin':
                return True

            tree = self._policyRepo.allTreeByRoleName(role)

