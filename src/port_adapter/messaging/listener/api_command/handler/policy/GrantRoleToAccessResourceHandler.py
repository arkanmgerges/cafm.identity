"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.port_adapter.messaging.listener.common.handler.policy.GrantRoleToAccessResourceHandler import \
    GrantRoleToAccessResourceHandler as Handler


class GrantRoleToAccessResourceHandler(Handler):
    def targetsOnException(self):
        return [Handler.targetOnException]
