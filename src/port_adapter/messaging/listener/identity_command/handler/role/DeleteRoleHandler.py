"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.RoleApplicationService import RoleApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import IdentityCommandConstant, CommonCommandConstant
from src.port_adapter.messaging.listener.identity_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class DeleteRoleHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.DELETE_ROLE

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{DeleteRoleHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: RoleApplicationService = AppDi.instance.get(RoleApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService.deleteRole(id=dataDict['id'], token=metadataDict['token'])
        return {'name': self._commandConstant.value, 'created_on': round(time.time() * 1000),
                'data': {'id': dataDict['id']},
                'metadata': metadataDict}

    def targetsOnSuccess(self):
        return [Handler.targetOnSuccess]