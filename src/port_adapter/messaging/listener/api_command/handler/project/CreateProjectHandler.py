"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.project.CreateProjectHandler import \
    CreateProjectHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreateProjectHandler, "CommonCommandConstant.CREATE_PROJECT.value", "api command consumer", "")
c4model:Rel(api__identity_project_py__create__api_command_topic, identity__messaging_api_command_handler__CreateProjectHandler, "CommonCommandConstant.CREATE_PROJECT.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreateProjectHandler, identity__domainmodel_event__ProjectCreated, "create")
"""


class CreateProjectHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]