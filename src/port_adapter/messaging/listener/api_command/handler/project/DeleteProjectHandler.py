"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.project.DeleteProjectHandler import \
    DeleteProjectHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteProjectHandler, "CommonCommandConstant.DELETE_PROJECT.value", "api command consumer", "")
c4model:Rel(api__identity_project_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteProjectHandler, "CommonCommandConstant.DELETE_PROJECT.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteProjectHandler, identity__domainmodel_event__ProjectDeleted, "create")
"""


class DeleteProjectHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
