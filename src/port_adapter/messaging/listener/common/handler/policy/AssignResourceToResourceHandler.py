"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class AssignResourceToResourceHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.ASSIGN_RESOURCE_TO_RESOURCE

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{AssignResourceToResourceHandler.handleMessage.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        appService: PolicyApplicationService = AppDi.instance.get(
            PolicyApplicationService
        )
        appService.assignResourceToResource(
            resourceSrcId=dataDict["src_resource_id"],
            resourceDstId=dataDict["dst_resource_id"],
            token=metadataDict["token"],
        )
        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": dataDict,
            "metadata": metadataDict,
        }
