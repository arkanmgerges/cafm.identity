"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)


class ProjectDoesNotExistException(DomainModelException):
    def __init__(self, message: str = ""):
        self.message = f"{message} does not exist"
        self.code = CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
        super().__init__(self.message, self.code)
