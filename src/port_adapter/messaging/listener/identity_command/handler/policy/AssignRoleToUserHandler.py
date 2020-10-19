"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class AssignRoleToUserHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == IdentityCommandConstant.ASSIGN_ROLE_TO_USER.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{AssignRoleToUserHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService.assignRoleToUser(roleId=dataDict['role_id'], userId=dataDict['user_id'], token=metadataDict['token'])
        return {'name': IdentityCommandConstant.ASSIGN_ROLE_TO_USER.value, 'createdOn': round(time.time() * 1000),
                'data': {'role_id': dataDict['role_id'], 'user_id': dataDict['user_id']},
                'metadata': metadataDict}
