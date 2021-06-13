"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from typing import Callable, List

from src.domain_model.event.EventConstant import CommonEventConstant
from src.port_adapter.messaging.listener.common.handler.project.UpdateProjectHandler import (
    UpdateProjectHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_project_event_handler__ProjectUpdatedHandler, "CommonEventConstant.PROJECT_UPDATED.value", "project event consumer", "")
c4model:Rel(identity__messaging_project_event_handler__ProjectUpdatedHandler, identity__domainmodel_event__ProjectUpdated, "create")
c4model:Rel(identity__messaging_project_event_handler__ProjectUpdatedHandler, project__domainmodel_event__ProjectUpdated, "consume")
"""


class ProjectUpdatedHandler(Handler):
    def canHandle(self, name: str) -> bool:
        return name == CommonEventConstant.PROJECT_UPDATED.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        data = messageData["data"]
        tmpDataDict = json.loads(data)
        old = tmpDataDict["old"]
        new = tmpDataDict["new"]
        dataDict = tmpDataDict["old"]
        dataDict["name"] = new["name"] if new["name"] is not None else old["name"]
        messageData["data"] = json.dumps(dataDict)
        return super().handleMessage(messageData)

    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
