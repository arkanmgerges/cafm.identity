"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from typing import Callable, List

from src.domain_model.event.EventConstant import CommonEventConstant
from src.port_adapter.messaging.listener.common.handler.realm.UpdateRealmHandler import (
    UpdateRealmHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_project_event_handler__OrganizationUpdatedHandler, "CommonEventConstant.ORGANIZATION_UPDATED.value", "project event consumer", "")
c4model:Rel(identity__messaging_project_event_handler__OrganizationUpdatedHandler, identity__domainmodel_event__RealmUpdated, "create")
c4model:Rel(identity__messaging_project_event_handler__OrganizationUpdatedHandler, project__domainmodel_event__OrganizationUpdated, "consume")
"""


class OrganizationUpdatedHandler(Handler):
    def canHandle(self, name: str) -> bool:
        return name == CommonEventConstant.ORGANIZATION_UPDATED.value

    def handleMessage(self, messageData: dict) -> dict:
        data = messageData["data"]
        dataDict = json.loads(data)
        dataDict = dataDict["new"]
        dataDict["realm_id"] = dataDict["organization_id"]
        messageData["data"] = json.dumps(dataDict)
        return super().handleMessage(messageData)

    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]
