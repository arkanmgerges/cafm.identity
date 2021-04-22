"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)


class DomainModelException(Exception):
    def __init__(
        self, message: str, code: int = CodeExceptionConstant.OBJECT_EXCEPTION.value
    ):
        self.message = f"domain model exception: {message}"
        self.code = code
        super().__init__(self.message)
