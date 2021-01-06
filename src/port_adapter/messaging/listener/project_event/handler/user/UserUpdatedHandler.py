"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.project_event.handler.Handler import Handler
from src.resource.logging.logger import logger


class UserUpdatedHandler(Handler):

    def __init__(self):
        self._eventConstant = CommonEventConstant.USER_UPDATED
        self._commandConstant = CommonCommandConstant.UPDATE_USER

    def canHandle(self, name: str) -> bool:
        return name == self._eventConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{UserUpdatedHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        currentUser = appService.userById(dataDict['new']['id'], token=metadataDict['token'])
        if currentUser.email() == dataDict['new']['email']:
            return {}

        return {'name': self._commandConstant.value, 'created_on': round(time.time() * 1000),
                'data': {'id': dataDict['new']['id'], 'email': dataDict['new']['email']},
                'metadata': metadataDict}
