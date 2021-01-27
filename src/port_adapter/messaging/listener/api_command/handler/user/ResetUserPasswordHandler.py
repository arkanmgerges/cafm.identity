"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant, \
    CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__ResetUserPasswordHandler, "Reset user password", "api command consumer", "Reset user password command")
c4model:Rel(identity__messaging_api_command_handler__ResetUserPasswordHandler, identity__messaging_identity_command_handler__GenerateUserOneTimePasswordHandler, "Reset user password", "message")
"""
class ResetUserPasswordHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.RESET_USER_PASSWORD

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{ResetUserPasswordHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        return {'name': CommonCommandConstant.GENERATE_USER_ONE_TIME_PASSWORD.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'id': dataDict['id'], 'email': dataDict['email']},
                'metadata': metadataDict}
