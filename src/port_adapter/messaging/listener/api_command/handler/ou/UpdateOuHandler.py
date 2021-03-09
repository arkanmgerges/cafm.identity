"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.ou.UpdateOuHandler import UpdateOuHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateOuHandler, "CommonCommandConstant.UPDATE_OU.value", "api command consumer", "")
c4model:Rel(api__identity_ou_py__update__api_command_topic, identity__messaging_api_command_handler__UpdateOuHandler, "CommonCommandConstant.UPDATE_OU.value", "message")
c4model:Rel(identity__messaging_api_command_handler__UpdateOuHandler, identity__domainmodel_event__OuUpdated, "create")
"""


class UpdateOuHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]