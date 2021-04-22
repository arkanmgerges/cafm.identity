"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.user.GenerateUserOneTimePasswordHandler import (
    GenerateUserOneTimePasswordHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__ResetUserPasswordHandler, "CommonCommandConstant.RESET_USER_PASSWORD.value", "api command consumer", "")
c4model:Rel(api__identity_user_py__resetUserPassword__api_command_topic, identity__messaging_api_command_handler__ResetUserPasswordHandler, "CommonCommandConstant.RESET_USER_PASSWORD.value", "message")
c4model:Rel(identity__messaging_api_command_handler__ResetUserPasswordHandler, identity__domainmodel_event__UserOneTimePasswordGenerated, "create")
"""


class ResetUserPasswordHandler(Handler):
    def canHandle(self, name: str) -> bool:
        return name == CommonCommandConstant.RESET_USER_PASSWORD.value

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]

    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
