"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateUserHandler, "Update user", "api command consumer", "Update command")
c4model:Rel(identity__messaging_api_command_handler__UpdateUserHandler, identity__messaging_identity_command_handler__UpdateUserHandler, "Update user", "message")
"""
class UpdateUserHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.UPDATE_USER

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{UpdateUserHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        # Put the command into the messaging system, in order to be processed later
        return {'name': self._commandConstant.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'id': dataDict['id'], 'name': dataDict['name'], 'password': dataDict['password'],
                         'first_name': dataDict['first_name'], 'last_name': dataDict['last_name'],
                         'address_one': dataDict['address_one'],
                         'address_two': dataDict['address_two'], 'postal_code': dataDict['postal_code'],
                         'avatar_image': dataDict['avatar_image']},
                'metadata': metadataDict}
