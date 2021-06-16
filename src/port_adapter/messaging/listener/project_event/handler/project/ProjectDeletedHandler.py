"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.event.EventConstant import CommonEventConstant
from src.port_adapter.messaging.listener.common.handler.project.DeleteProjectHandler import (
    DeleteProjectHandler as Handler,
)


class ProjectDeletedHandler(Handler):
    def canHandle(self, name: str) -> bool:
        return name == CommonEventConstant.PROJECT_DELETED.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        return super().handleMessage(messageData=messageData, extraData=extraData)