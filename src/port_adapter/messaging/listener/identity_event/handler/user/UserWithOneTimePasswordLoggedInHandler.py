"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.project_event.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger

"""
c4model|cb|identity:ComponentQueue(identity__messaging_identity_event_handler__UserWithOneTimePasswordLoggedInHandler, "User with one time password logged in", "identity event consumer", "User one time password logged in")
c4model:Rel(identity__messaging_identity_event_handler__UserWithOneTimePasswordLoggedInHandler, identity__messaging_identity_command_handler__DeleteUserOneTimePasswordHandler, "Send email one time user password", "message")
"""
class UserWithOneTimePasswordLoggedInHandler(Handler):

    def __init__(self):
        self._eventConstant = CommonEventConstant.USER_WITH_ONE_TIME_PASSWORD_LOGGED_IN
        self._commandConstant = CommonCommandConstant.DELETE_USER_ONE_TIME_PASSWORD

    def canHandle(self, name: str) -> bool:
        return name == self._eventConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{UserWithOneTimePasswordLoggedInHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        return {'name': self._commandConstant.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'user_id': dataDict['user_id']},
                'metadata': metadataDict}
