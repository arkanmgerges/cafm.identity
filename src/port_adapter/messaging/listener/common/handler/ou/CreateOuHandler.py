"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.OuApplicationService import OuApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class CreateOuHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.CREATE_OU

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{CreateOuHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: OuApplicationService = AppDi.instance.get(OuApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        obj = appService.createOu(id=None, name=dataDict['name'], token=metadataDict['token'])
        return {'name': self._commandConstant.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'id': obj.id(), 'name': obj.name()},
                'metadata': metadataDict}

    def targetsOnSuccess(self):
        return [Handler.targetOnSuccess]

    def targetsOnException(self):
        return [Handler.targetOnException]
