"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.RevokeAssignmentRoleToPermissionHandler import \
    RevokeAssignmentRoleToPermissionHandler as Handler


class RevokeAssignmentRoleToPermissionHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
