"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class InvalidValueException(DomainModelException):
    def __init__(self, message:str = ''):
        self.message = f'Invalid value: {message}'
        self.code = CodeExceptionConstant.OBJECT_CASTING_ERROR.value
        super().__init__(self.message, self.code)
