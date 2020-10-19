"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class RevokeAssignmentUserToUserGroupHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == ApiCommandConstant.REVOKE_ASSIGNMENT_USER_TO_USER_GROUP.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{RevokeAssignmentUserToUserGroupHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        return {'name': IdentityCommandConstant.REVOKE_ASSIGNMENT_USER_TO_USER_GROUP.value, 'createdOn': round(time.time() * 1000),
                'data': {'user_id': dataDict['user_id'], 'user_group_id': dataDict['user_group_id']},
                'metadata': metadataDict}
