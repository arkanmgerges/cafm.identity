"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.user_group.DeleteUserGroupHandler import (
    DeleteUserGroupHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteUserGroupHandler, "CommonCommandConstant.DELETE_USER_GROUP.value", "api command consumer", "")
c4model:Rel(api__identity_user_group_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteUserGroupHandler, "CommonCommandConstant.DELETE_USER_GROUP.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteUserGroupHandler, identity__domainmodel_event__UserGroupDeleted, "create")
"""


class DeleteUserGroupHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
