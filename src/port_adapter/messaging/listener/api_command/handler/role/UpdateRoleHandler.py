"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.role.UpdateRoleHandler import UpdateRoleHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateRoleHandler, "CommonCommandConstant.UPDATE_ROLE.value", "api command consumer", "")
c4model:Rel(api__identity_role_py__update__api_command_topic, identity__messaging_api_command_handler__UpdateRoleHandler, "CommonCommandConstant.UPDATE_ROLE.value", "message")
c4model:Rel(identity__messaging_api_command_handler__UpdateRoleHandler, identity__domainmodel_event__RoleUpdated, "create")
"""


class UpdateRoleHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]