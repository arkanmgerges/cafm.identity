"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import IdentityCommandConstant, CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class UpdateUserHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.UPDATE_USER

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{UpdateUserHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService.updateUser(id=dataDict['id'], name=dataDict['name'],
                              firstName=dataDict['first_name'], lastName=dataDict['last_name'], 
                              addressOne=dataDict['address_one'], addressTwo=dataDict['address_two'], 
                              postalCode=dataDict['postal_code'], avatarImage=dataDict['avatar_image'],
                              token=metadataDict['token'])
        return {'name': self._commandConstant.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': dataDict['id'], 'name': dataDict['name'], 'password': dataDict['password'],
                         'firstName': dataDict['firstName'], 'lastName': dataDict['lastName'], 'addressOne': dataDict['addressOne'],
                         'addressTwo': dataDict['addressTwo'], 'postalCode': dataDict['postalCode'], 'avatarImage': dataDict['avatarImage']},
                'metadata': metadataDict}
