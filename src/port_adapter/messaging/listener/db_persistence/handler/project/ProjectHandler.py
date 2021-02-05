"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from typing import List, Callable

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.project.Project import Project
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.port_adapter.messaging.listener.db_persistence.handler.common.Util import Util
from src.resource.logging.logger import logger


class ProjectHandler(Handler):
    def __init__(self):
        import src.port_adapter.AppDi as AppDi
        self._eventConstants = [
            CommonEventConstant.PROJECT_CREATED.value,
            CommonEventConstant.PROJECT_UPDATED.value,
            CommonEventConstant.PROJECT_DELETED.value,
        ]
        self._repository: ProjectRepository = AppDi.instance.get(ProjectRepository)

    def canHandle(self, name: str) -> bool:
        return name in self._eventConstants

    def handleCommand(self, messageData: dict):
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{ProjectHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        # metadataDict = json.loads(metadata)
        #
        # if 'token' not in metadataDict:
        #     raise UnAuthorizedException()

        result = self.execute(name, **dataDict)
        return {'data': result, 'metadata': metadata}

    def execute(self, event, *args, **kwargs):
        funcSwitcher = {
            CommonEventConstant.PROJECT_CREATED.value: self._save,
            CommonEventConstant.PROJECT_UPDATED.value: self._save,
            CommonEventConstant.PROJECT_DELETED.value: self._delete,
        }

        argSwitcher = {
            CommonEventConstant.PROJECT_CREATED.value: lambda: {
                'obj': Project.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs))},
            CommonEventConstant.PROJECT_UPDATED.value: lambda: {
                'obj': Project.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs['new']))},
            CommonEventConstant.PROJECT_DELETED.value: lambda: {
                'obj': Project.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs))},
        }
        func = funcSwitcher.get(event, None)
        if func is not None:
            # Execute the function with the arguments
            return func(*args, **(argSwitcher.get(event))())
        return None

    def _save(self, *_args, obj: Project):
        self._repository.save(obj=obj)
        return obj.toMap()

    def _delete(self, *_args, obj: Project):
        self._repository.deleteProject(obj=obj)
        return obj.toMap()

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]