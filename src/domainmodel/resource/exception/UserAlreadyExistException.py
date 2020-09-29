"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.DomainModelException import DomainModelException
from src.domainmodel.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class UserAlreadyExistException(DomainModelException):
    def __init__(self, username: str = ''):
        self.message = f'{username} already exist'
        self.code = CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        super().__init__(self.message, self.code)
