"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.AssignRoleToUserHandler import AssignRoleToUserHandler as Handler


class AssignRoleToUserHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
