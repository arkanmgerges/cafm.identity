"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant, \
    CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class RevokeAssignmentRoleToPermissionForResourceTypeHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.REVOKE_ASSIGNMENT_ROLE_TO_PERMISSION_FOR_RESOURCE_TYPE

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{RevokeAssignmentRoleToPermissionForResourceTypeHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        return {'name': self._commandConstant.value,
                'createdOn': round(time.time() * 1000),
                'data': {'role_id': dataDict['role_id'], 'permission_id': dataDict['permission_id'],
                         'resource_type_id': dataDict['resource_type_id']},
                'metadata': metadataDict}
