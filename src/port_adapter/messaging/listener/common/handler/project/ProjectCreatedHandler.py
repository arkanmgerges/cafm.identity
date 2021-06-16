"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from src.resource.common.Util import Util

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class ProjectCreatedHandler(Handler):
    def __init__(self):
        self._eventConstant = CommonEventConstant.PROJECT_CREATED
        self._commandConstant = CommonCommandConstant.CREATE_ROLE_FOR_PROJECT_ACCESS

    def canHandle(self, name: str) -> bool:
        return name == self._eventConstant.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{ProjectCreatedHandler.handleMessage.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        appService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)

        roleDataDict = {"id": appService.newId(), "name": "access-"+dataDict["project_id"], "title": "access-"+dataDict["project_id"], "project_id": dataDict["project_id"]}

        # appService.createRoleForProject(**Util.snakeCaseToLowerCameCaseDict(roleDataDict), token=metadataDict["token"])

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": roleDataDict,
            "metadata": metadataDict,
        }

