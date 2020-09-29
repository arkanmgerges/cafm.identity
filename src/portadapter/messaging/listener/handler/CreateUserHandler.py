"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.portadapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.portadapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant
from src.portadapter.messaging.listener.handler.Handler import Handler
from src.resource.logging.logger import logger


class CreateUserHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == ApiCommandConstant.CREATE_USER.value

    def handleCommand(self, name: str, data: str) -> dict:
        logger.debug(
            f'handle command received args - name: {name}, type(name): {type(name)}, data: {data}, type(data): {type(data)}')
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        obj = appService.createObjectOnly(username=dataDict['username'], password=dataDict['password'])
        return {'name': IdentityCommandConstant.CREATE_USER.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': obj.id(), 'username': obj.username(), 'password': obj.password()}}
