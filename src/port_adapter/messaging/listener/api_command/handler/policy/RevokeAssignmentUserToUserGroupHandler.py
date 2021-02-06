"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.RevokeAssignmentUserToUserGroupHandler import \
    RevokeAssignmentUserToUserGroupHandler as Handler


class RevokeAssignmentUserToUserGroupHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
