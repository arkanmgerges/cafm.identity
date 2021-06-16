"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.project.ProjectCreatedHandler import (
    ProjectCreatedHandler as Handler,
)
from src.resource.logging.logger import logger

"""
c4model|cb|project:ComponentQueue(project__messaging_identity_event_handler__ProjectCreatedHandler, "CommonEventConstant.PROJECT_CREATED.value", "identity event consumer", "")
c4model:Rel(project__messaging_identity_event_handler__ProjectCreatedHandler, identity__domainmodel_event__ProjectCreated, "consume")
c4model:Rel(project__messaging_identity_event_handler__ProjectCreatedHandler, project__messaging_project_command_handler__CreateProjectHandler, "CommonCommandConstant.CREATE_PROJECT.value", "message")
"""


class ProjectCreatedHandler(Handler):
    def canHandle(self, name: str) -> bool:
        from src.domain_model.event.EventConstant import CommonEventConstant
        return name == CommonEventConstant.PROJECT_CREATED.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        return super().handleMessage(messageData=messageData, extraData=extraData)
