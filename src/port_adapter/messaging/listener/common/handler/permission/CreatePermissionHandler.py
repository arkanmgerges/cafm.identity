"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.PermissionApplicationService import PermissionApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class CreatePermissionHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.CREATE_PERMISSION

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{CreatePermissionHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        appService: PermissionApplicationService = AppDi.instance.get(
            PermissionApplicationService
        )
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        id = dataDict["permission_id"] if "permission_id" in dataDict else None
        obj = appService.createPermission(
            id=id,
            name=dataDict["name"],
            allowedActions=dataDict["allowed_actions"],
            deniedActions=dataDict["denied_actions"],
            token=metadataDict["token"],
        )
        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": {
                "permission_id": obj.id(),
                "name": obj.name(),
                "allowed_actions": obj.allowedActions(),
                "denied_actions": obj.deniedActions(),
            },
            "metadata": metadataDict,
        }
