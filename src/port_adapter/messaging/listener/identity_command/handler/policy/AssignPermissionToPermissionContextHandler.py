"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class AssignPermissionToPermissionContextHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.ASSIGN_PERMISSION_TO_PERMISSION_CONTEXT

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{AssignPermissionToPermissionContextHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: PolicyApplicationService = AppDi.instance.get(PolicyApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        appService.assignPermissionToPermissionContext(permissionId=dataDict['permission_id'],
                                                  permissionContextId=dataDict['permission_context_id'],
                                                  token=metadataDict['token'])
        return {'name': self._commandConstant.value,
                'createdOn': round(time.time() * 1000),
                'data': {'permission_id': dataDict['permission_id'],
                         'permission_context_id': dataDict['permission_context_id']},
                'metadata': metadataDict}
