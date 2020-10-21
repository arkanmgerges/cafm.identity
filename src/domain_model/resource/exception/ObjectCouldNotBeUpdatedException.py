"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class ObjectCouldNotBeUpdatedException(DomainModelException):
    def __init__(self, message: str = ''):
        self.message = f'{message} Could not updated the object'
        self.code = CodeExceptionConstant.OBJECT_COULD_NOT_BE_UPDATED.value
        super().__init__(self.message, self.code)
