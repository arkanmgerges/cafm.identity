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
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger

"""
c4model|cb|identity:ComponentQueue(identity__messaging_project_event_handler__UserUpdatedHandler, "User updated by the project", "project event consumer", "User updated by project")
c4model:Rel(identity__messaging_project_event_handler__UserUpdatedHandler, identity__messaging_identity_command_handler__UpdateUserHandler, "Update user", "message")
"""
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

        return {'name': self._commandConstant.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'id': dataDict['new']['id'], 'email': dataDict['new']['email']},
                'metadata': metadataDict}
