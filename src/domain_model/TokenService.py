"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

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

    def generateToken(self, payload: dict) -> str:
        """Generate token by payload

        Args:
            payload (dict): Data that is used to generate the token

        Returns:
            str: Token string
        """
        header = {'alg': 'HS256'}
        key = os.getenv('CAFM_JWT_SECRET', 'secret')
        import uuid
        payload['_token_gen_num'] = str(uuid.uuid1())
        token = jwt.encode(header, payload, key).decode('utf-8')
        return token
