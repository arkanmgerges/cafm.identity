"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.user.CreateUserHandler import (
    CreateUserHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreateUserHandler, "CommonCommandConstant.CREATE_USER.value", "api command consumer", "")
c4model:Rel(api__identity_user_py__create__api_command_topic, identity__messaging_api_command_handler__CreateUserHandler, "CommonCommandConstant.CREATE_USER.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreateUserHandler, identity__domainmodel_event__UserCreated, "create")
"""


class CreateUserHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
