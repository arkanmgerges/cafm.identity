"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.user.User import User
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.identity_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class CreateUserHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.CREATE_USER

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{CreateUserHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        obj: User = appService.createUser(id=dataDict['id'], name=dataDict['name'], password=dataDict['password'],
                                          firstName=dataDict['first_name'], lastName=dataDict['last_name'],
                                          addressOne=dataDict['address_one'], addressTwo=dataDict['address_two'],
                                          postalCode=dataDict['postal_code'], avatarImage=dataDict['avatar_image'],
                                          token=metadataDict['token'])
        return {'name': self._commandConstant.value, 'created_on': round(time.time() * 1000),
                'data': {'id': obj.id(), 'name': obj.name(), 'first_name': obj.firstName(),
                         'last_name': obj.lastName(), 'address_one': obj.addressOne(), 'address_two': obj.addressTwo(),
                         'postal_code': obj.postalCode(), 'avatar_image': obj.avatarImage()},
                'metadata': metadataDict}

    def targetsOnSuccess(self):
        return [Handler.targetOnSuccess]

    def targetsOnException(self):
        return [Handler.targetOnException]
