"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)


class ProcessBulkDomainException(DomainModelException):
    def __init__(self, messages: List[dict]):
        self.message = "Bulk processing exceptions"
        self.extra = messages
        self.code = CodeExceptionConstant.PROCESS_BULK_EXCEPTION.value
        super().__init__(self.message, self.code, self.extra)
