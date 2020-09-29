"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domainmodel.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class DomainModelException(Exception):
    def __init__(self, msg: str, code: int = CodeExceptionConstant.OBJECT_EXCEPTION.value):
        self.message = f'domain model exception: {msg}'
        self.code = code
        super().__init__(self.message)
