"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from authlib.jose import jwt

from src.domain_model.token.TokenData import TokenData
from src.resource.logging.logger import logger


class TokenService:
    @staticmethod
    def claimsFromToken(token: str) -> dict:
        """Get claims by decoding and validating the token

        Args:
            token (str): Token that can carry the info about a user

        Returns:
            dict: A dictionary that represents the claims of the token
            e.g. {"id": "1234", "role": ["super_admin", "accountant"], "name": "john"}

        :raises:
            `BadSignatureError <authlib.jose.errors.BadSignatureError>` If the token is invalid
        """
        logger.debug(f'[{TokenService.claimsFromToken.__qualname__}] Received token: {token}')
        import os
        key = os.getenv('CAFM_JWT_SECRET', 'secret')
        claims = jwt.decode(token, key)
        claims.validate()
        return claims

    @staticmethod
    def generateToken(payload: dict) -> str:
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

    @staticmethod
    def tokenDataFromToken(token: str) -> TokenData:
        """Get token data by decoding and validating the token

        Args:
            token (str): Token that can carry the payload

        Returns:
            TokenData: A token data object

        :raises:
            `BadSignatureError <authlib.jose.errors.BadSignatureError>` If the token is invalid
        """
        logger.debug(f'[{TokenService.tokenDataFromToken.__qualname__}] Received token: {token}')
        dictData = TokenService.claimsFromToken(token=token)
        return TokenData(id=dictData['id'], name=dictData['name'], roles=dictData['roles'])

    @staticmethod
    def isSuperAdmin(tokenData: TokenData):
        role = tokenData.roles()
        for i in role:
            if i['name'] == 'super_admin':
                return True
        return False
