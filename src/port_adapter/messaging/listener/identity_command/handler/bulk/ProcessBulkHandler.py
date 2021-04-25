"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import Callable, List

from src.port_adapter.messaging.listener.common.handler.bulk.ProcessBulkHandler import (
    ProcessBulkHandler as Handler,
)


class ProcessBulkHandler(Handler):
    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
