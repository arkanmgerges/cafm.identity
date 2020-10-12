"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.AuthorizationService import AuthorizationService


class AuthorizationApplicationService:
    def __init__(self, authzService: AuthorizationService):
        self._authzService: AuthorizationService = authzService

    def isAllowed(self, token: str, action: str = '', resourceType: str = '', resourceId: str = None) -> bool:
        """Check if the token has access to the context provided by data

        Args:
            token (str): Token that is used for authorization check
            action (str): An action that can be applied over the resource or/and resource type
            resourceType (str): The type of the resource that the action will be applied to
            resourceId (str): The id of the resource that the action will be applied to


        Returns:
            bool: True if the token has access or False otherwise
        """
        return self._authzService.isAllowed(token=token, action=action, resourceType=resourceType,
                                            resourceId=resourceId)
