"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.OuApplicationService import OuApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class CreateOuHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == IdentityCommandConstant.CREATE_OU.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{CreateOuHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: OuApplicationService = AppDi.instance.get(OuApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        obj = appService.createOu(id=dataDict['id'], name=dataDict['name'], token=metadataDict['token'])
        return {'name': IdentityCommandConstant.CREATE_OU.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': obj.id(), 'name': obj.name()},
                'metadata': metadataDict}
