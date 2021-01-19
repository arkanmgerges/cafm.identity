"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class RevokeAssignmentResourceToResourceHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.REVOKE_ASSIGNMENT_RESOURCE_TO_RESOURCE

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{RevokeAssignmentResourceToResourceHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        return {'name': self._commandConstant.value, 'created_on': DateTimeHelper.utcNow(),
                'data': {'src_resource_id': dataDict['src_resource_id'],
                         'dst_resource_id': dataDict['dst_resource_id']},
                'metadata': metadataDict}
