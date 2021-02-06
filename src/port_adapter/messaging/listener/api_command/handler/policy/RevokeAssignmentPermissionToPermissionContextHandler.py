"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.RevokeAssignmentPermissionToPermissionContextHandler import \
    RevokeAssignmentPermissionToPermissionContextHandler as Handler


class RevokeAssignmentPermissionToPermissionContextHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
