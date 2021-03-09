"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.permission.UpdatePermissionHandler import \
    UpdatePermissionHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdatePermissionHandler, "CommonCommandConstant.UPDATE_PERMISSION.value", "api command consumer", "")
c4model:Rel(api__identity_permission_py__update__api_command_topic, identity__messaging_api_command_handler__UpdatePermissionHandler, "CommonCommandConstant.UPDATE_PERMISSION.value", "message")
c4model:Rel(identity__messaging_api_command_handler__UpdatePermissionHandler, identity__domainmodel_event__PermissionUpdated, "create")
"""


class UpdatePermissionHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]