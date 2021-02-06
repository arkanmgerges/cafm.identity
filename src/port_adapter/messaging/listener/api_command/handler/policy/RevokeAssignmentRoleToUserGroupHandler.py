"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.RevokeAssignmentRoleToUserGroupHandler import \
    RevokeAssignmentRoleToUserGroupHandler as Handler


class RevokeAssignmentRoleToUserGroupHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
