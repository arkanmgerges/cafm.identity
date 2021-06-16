"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from src.resource.common.Util import Util

import src.port_adapter.AppDi as AppDi
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class RoleCreatedForProjectHandler(Handler):
    def __init__(self):
        self._eventConstant = CommonEventConstant.PROJECT_CREATED
        self._commandConstant = CommonCommandConstant.DUMMY_PROJECT

    def canHandle(self, name: str) -> bool:
        return name == self._eventConstant.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{RoleCreatedForProjectHandler.handleMessage.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
        appService.assignResourceToResource(resourceSrcId=dataDict["role_id"], resourceDstId=dataDict["project_id"], token=metadataDict["token"])

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        return None
