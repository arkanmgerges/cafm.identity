"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class NotAllowedAccessAssignmentException(DomainModelException):
    def __init__(self, message: str = ''):
        self.message = f'{message} not allowed access assignment'
        self.code = CodeExceptionConstant.NOT_ALLOWED_ACCESS_ASSIGNMENT.value
        super().__init__(self.message, self.code)
