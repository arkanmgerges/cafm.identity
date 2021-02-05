"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from typing import List, Callable

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.permission.Permission import Permission
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.port_adapter.messaging.listener.db_persistence.handler.common.Util import Util
from src.resource.logging.logger import logger


class PermissionHandler(Handler):
    def __init__(self):
        import src.port_adapter.AppDi as AppDi
        self._eventConstants = [
            CommonEventConstant.PERMISSION_CREATED.value,
            CommonEventConstant.PERMISSION_UPDATED.value,
            CommonEventConstant.PERMISSION_DELETED.value,
        ]
        self._repository: PermissionRepository = AppDi.instance.get(PermissionRepository)

    def canHandle(self, name: str) -> bool:
        return name in self._eventConstants

    def handleCommand(self, messageData: dict):
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{PermissionHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        dataDict = json.loads(data)
        # metadataDict = json.loads(metadata)
        #
        # if 'token' not in metadataDict:
        #     raise UnAuthorizedException()

        result = self.execute(name, **dataDict)
        return {'data': result, 'metadata': metadata}

    def execute(self, event, *args, **kwargs):
        funcSwitcher = {
            CommonEventConstant.PERMISSION_CREATED.value: self._save,
            CommonEventConstant.PERMISSION_UPDATED.value: self._save,
            CommonEventConstant.PERMISSION_DELETED.value: self._delete,
        }

        argSwitcher = {
            CommonEventConstant.PERMISSION_CREATED.value: lambda: {
                'obj': Permission.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs))},
            CommonEventConstant.PERMISSION_UPDATED.value: lambda: {
                'obj': Permission.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs['new']))},
            CommonEventConstant.PERMISSION_DELETED.value: lambda: {
                'obj': Permission.createFrom(**Util.snakeCaseToLowerCameCaseDict(kwargs))},
        }
        func = funcSwitcher.get(event, None)
        if func is not None:
            # Execute the function with the arguments
            return func(*args, **(argSwitcher.get(event))())
        return None

    def _save(self, *_args, obj: Permission):
        self._repository.save(obj=obj)
        return obj.toMap()

    def _delete(self, *_args, obj: Permission):
        self._repository.deletePermission(obj=obj)
        return obj.toMap()

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]