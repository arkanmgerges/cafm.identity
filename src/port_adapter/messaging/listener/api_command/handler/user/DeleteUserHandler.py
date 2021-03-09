"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.user.DeleteUserHandler import DeleteUserHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteUserHandler, "CommonCommandConstant.DELETE_USER.value", "api command consumer", "")
c4model:Rel(api__identity_user_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteUserHandler, "CommonCommandConstant.DELETE_USER.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteUserHandler, identity__domainmodel_event__UserDeleted, "create")
"""


class DeleteUserHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]