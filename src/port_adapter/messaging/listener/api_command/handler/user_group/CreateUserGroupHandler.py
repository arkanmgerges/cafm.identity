"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.user_group.CreateUserGroupHandler import \
    CreateUserGroupHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreateUserGroupHandler, "CommonCommandConstant.CREATE_USER_GROUP.value", "api command consumer", "")
c4model:Rel(api__identity_user_group_py__create__api_command_topic, identity__messaging_api_command_handler__CreateUserGroupHandler, "CommonCommandConstant.CREATE_USER_GROUP.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreateUserGroupHandler, identity__domainmodel_event__UserGroupCreated, "create")
"""


class CreateUserGroupHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
