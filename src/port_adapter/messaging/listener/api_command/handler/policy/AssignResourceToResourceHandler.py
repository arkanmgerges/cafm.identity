"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.policy.AssignResourceToResourceHandler import \
    AssignResourceToResourceHandler as Handler


class AssignResourceToResourceHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]