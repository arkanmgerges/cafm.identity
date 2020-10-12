"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class DeleteUserGroupHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == IdentityCommandConstant.DELETE_USER_GROUP.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{DeleteUserGroupHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: UserGroupApplicationService = AppDi.instance.get(UserGroupApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService.deleteUserGroup(id=dataDict['id'], token=metadataDict['token'])
        return {'name': IdentityCommandConstant.DELETE_USER_GROUP.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': dataDict['id']},
                'metadata': metadataDict}
