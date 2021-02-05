"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.role.CreateRoleHandler import CreateRoleHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreateRoleHandler, "CommonCommandConstant.CREATE_ROLE.value", "api command consumer", "")
c4model:Rel(api__identity_role_py__create__api_command_topic, identity__messaging_api_command_handler__CreateRoleHandler, "CommonCommandConstant.CREATE_ROLE.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreateRoleHandler, identity__domainmodel_event__RoleCreated, "create")
"""


class CreateRoleHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
