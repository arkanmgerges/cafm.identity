"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class CreateUserHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == ApiCommandConstant.CREATE_USER.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{CreateUserHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)
        obj = appService.createObjectOnly(name=dataDict['name'], password=dataDict['password'])
        return {'name': IdentityCommandConstant.CREATE_USER.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': obj.id(), 'name': obj.name(), 'password': obj.password()},
                'metadata': metadataDict}
