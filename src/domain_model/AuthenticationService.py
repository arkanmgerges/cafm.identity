"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.AuthenticationRepository import AuthenticationRepository
from authlib.jose import jwt


class AuthenticationService:
    def __init__(self, authRepo: AuthenticationRepository):
        self._authRepo = authRepo

    def authenticateUser(self, name: str, password: str) -> str:
        """Authenticate user and return jwt token

        Args:
            name (str): User name
            password (str): User password

        Return:
            str: Authentication token

        :raises:
            `UserDoesNotExistException <UserDoesNotExistException>`: When user does not exist
        """
        result = self._authRepo.authenticateUserByNameAndPassword(name=name, password=password)
        header = {'alg': 'HS256'}
        payload = {'id': result['id'], 'role': result['role'], 'name': result['name']}
        import os
        key = os.getenv('CAFM_JWT_SECRET', 'secret')
        token = jwt.encode(header, payload, key).decode('utf-8')
        self._authRepo.persistToken(token=token)
        return token
