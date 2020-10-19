"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class InvalidCredentialsException(DomainModelException):
    def __init__(self, message:str = ''):
        self.message = f'Invalid credentials for user {message}'
        self.code = CodeExceptionConstant.INVALID_CREDENTIALS.value
        super().__init__(self.message, self.code)
