"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class UpdateRoleHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.UPDATE_ROLE

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict, extraData: dict = None) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{UpdateRoleHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        appService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        appService.updateRole(
            id=dataDict["role_id"], name=dataDict["name"], token=metadataDict["token"]
        )
        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": {"role_id": dataDict["role_id"], "name": dataDict["name"]},
            "metadata": metadataDict,
        }
