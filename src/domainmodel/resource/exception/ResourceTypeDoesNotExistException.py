"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.DomainModelException import DomainModelException
from src.domainmodel.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class ResourceTypeDoesNotExistException(DomainModelException):
    def __init__(self, name:str = ''):
        self.message = f'{name} does not exist'
        self.code = CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
        super().__init__(self.message, self.code)
