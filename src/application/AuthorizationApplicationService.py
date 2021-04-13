"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Dict

from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.resource.logging.decorator import debugLogger


class AuthorizationApplicationService:
    def __init__(self, authzService: AuthorizationService):
        self._authzService: AuthorizationService = authzService

    @debugLogger
    def hashKeys(self, keys: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Hash the key list

        Args:
            keys (List[Dict[str, str]]): It is a list of dictionary with keys that have the value as 'key'

        Returns:
            List[Dict[str, str]]: A list of dictionary where each item has two keys, one is 'key' and the other is
                                  hashCode
        """
        return self._authzService.hashKeys(keys=keys)
