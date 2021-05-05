"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)


class InvalidAttributeException(DomainModelException):
    def __init__(self, message: str = ""):
        self.message = f"{message}"
        self.code = CodeExceptionConstant.INVALID_ATTRIBUTE.value
        super().__init__(self.message, self.code)
