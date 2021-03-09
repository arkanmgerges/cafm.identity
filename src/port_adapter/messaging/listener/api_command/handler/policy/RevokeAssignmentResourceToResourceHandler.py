"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import Callable, List

from src.port_adapter.messaging.listener.common.handler.policy.RevokeAssignmentResourceToResourceHandler import \
    RevokeAssignmentResourceToResourceHandler as Handler


class RevokeAssignmentResourceToResourceHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]