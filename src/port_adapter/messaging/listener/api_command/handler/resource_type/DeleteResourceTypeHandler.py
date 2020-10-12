"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class DeleteResourceTypeHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == ApiCommandConstant.DELETE_RESOURCE_TYPE.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{DeleteResourceTypeHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: ResourceTypeApplicationService = AppDi.instance.get(ResourceTypeApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        # Put the command into the messaging system, in order to be processed later
        return {'name': IdentityCommandConstant.DELETE_RESOURCE_TYPE.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': dataDict['id']},
                'metadata': metadataDict}
