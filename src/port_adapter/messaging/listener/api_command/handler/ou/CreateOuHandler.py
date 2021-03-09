"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.ou.CreateOuHandler import CreateOuHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreateOuHandler, "CommonCommandConstant.CREATE_OU.value", "api command consumer", "")
c4model:Rel(api__identity_ou_py__create__api_command_topic, identity__messaging_api_command_handler__CreateOuHandler, "CommonCommandConstant.CREATE_OU.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreateOuHandler, identity__domainmodel_event__OuCreated, "create")
"""


class CreateOuHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]