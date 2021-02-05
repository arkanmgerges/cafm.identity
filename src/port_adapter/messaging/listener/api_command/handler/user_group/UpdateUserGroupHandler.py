"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import Callable, List

from src.port_adapter.messaging.listener.common.handler.user_group.UpdateUserGroupHandler import UpdateUserGroupHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateUserGroupHandler, "CommonCommandConstant.UPDATE_USER_GROUP.value", "api command consumer", "")
c4model:Rel(api__identity_user_group_py__update__api_command_topic, identity__messaging_api_command_handler__UpdateUserGroupHandler, "CommonCommandConstant.UPDATE_USER_GROUP.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteUserGroupHandler, identity__domainmodel_event__UserGroupUpdated, "create")
"""


class UpdateUserGroupHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
