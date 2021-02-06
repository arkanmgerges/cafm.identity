"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.AssignUserToUserGroupHandler import \
    AssignUserToUserGroupHandler as Handler


class AssignUserToUserGroupHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
