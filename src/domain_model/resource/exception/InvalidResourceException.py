"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class InvalidResourceException(DomainModelException):
    def __init__(self, message:str = ''):
        self.message = f'Invalid resource: {message}'
        self.code = CodeExceptionConstant.INVALID_RESOURCE.value
        super().__init__(self.message, self.code)
