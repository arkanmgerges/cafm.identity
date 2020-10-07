"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from authlib.jose import jwt

from src.resource.logging.logger import logger


class TokenService:
    def claimsFromToken(self, token: str) -> dict:
        """Get claims by decoding and validating the token

        Args:
            token (str): Token that can carry the info about a user

        Returns:
            dict: A dictionary that represents the claims of the token
            e.g. {"id": "1234", "role": ["super_admin", "accountant"], "name": "john"}

        :raises:
            `BadSignatureError <authlib.jose.errors.BadSignatureError>` If the token is invalid
        """
        logger.debug(f'[{TokenService.claimsFromToken.__qualname__}] - Received token: {token}')
        import os
        key = os.getenv('CAFM_JWT_SECRET', 'secret')
        claims = jwt.decode(token, key)
        claims.validate()
        return claims
