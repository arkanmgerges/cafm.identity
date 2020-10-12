"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.ProjectApplicationService import ProjectApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.port_adapter.messaging.listener.CommandConstant import ApiCommandConstant, IdentityCommandConstant
from src.port_adapter.messaging.listener.api_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class UpdateProjectHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == ApiCommandConstant.UPDATE_PROJECT.value

    def handleCommand(self, name: str, data: str, metadata: str) -> dict:
        logger.debug(
            f'[{UpdateProjectHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: ProjectApplicationService = AppDi.instance.get(ProjectApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        # Put the command into the messaging system, in order to be processed later
        return {'name': IdentityCommandConstant.UPDATE_PROJECT.value, 'createdOn': round(time.time() * 1000),
                'data': {'id': dataDict['id'], 'name': dataDict['name']},
                'metadata': metadataDict}
