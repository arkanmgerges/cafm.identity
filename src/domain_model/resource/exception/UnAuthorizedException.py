"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class UnAuthorizedException(DomainModelException):
    def __init__(self):
        self.message = f'Un authorized action'
        self.code = CodeExceptionConstant.UN_AUTHORIZED_ACTION.value
        super().__init__(self.message, self.code)
