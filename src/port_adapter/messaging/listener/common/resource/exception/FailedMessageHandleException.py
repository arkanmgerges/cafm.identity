"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.port_adapter.messaging.listener.common.resource.exception.CodeExceptionConstant import CodeExceptionConstant


class FailedMessageHandleException(Exception):
    def __init__(
        self, message: str, code: int = CodeExceptionConstant.FAILED_MESSAGE_HANDLE_EXCEPTION.value,
            extra: List[dict] = None,
    ):
        self.message = f"failed message handle exception: {message}"
        self.extra = extra
        self.code = code
        super().__init__(self.message)
