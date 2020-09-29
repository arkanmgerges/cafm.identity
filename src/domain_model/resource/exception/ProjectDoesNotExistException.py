"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class ProjectDoesNotExistException(DomainModelException):
    def __init__(self, name:str = ''):
        self.message = f'{name} does not exist'
        self.code = CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
        super().__init__(self.message, self.code)
