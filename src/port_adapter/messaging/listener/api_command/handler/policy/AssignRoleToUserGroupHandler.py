"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.AssignRoleToUserGroupHandler import \
    AssignRoleToUserGroupHandler as Handler


class AssignRoleToUserGroupHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
