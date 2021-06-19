"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.PermissionApplicationService import PermissionApplicationService
from src.application.PermissionContextApplicationService import PermissionContextApplicationService
from src.application.PolicyApplicationService import PolicyApplicationService
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.domain_model.resource.exception.ProcessBulkDomainException import ProcessBulkDomainException


class ProcessBulkHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.PROCESS_BULK
        self._handlers = []

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        data = messageData["data"]
        metadata = messageData["metadata"]

        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        totalItemCount = dataDict["total_item_count"]
        try:
            # The is the final result of all the data items in the dataDict["data"]
            dataDict["data"].sort(key=self._sortKeyByCommand)
            batchedDataItems = self._batchSimilar(dataDict["data"])
            for batchedDataCommand, batchedDataValue in batchedDataItems.items():
                entityName = batchedDataCommand[batchedDataCommand.index("_") + 1:]
                appService = self._appServiceByEntityName(entityName)
                commandMethod = batchedDataCommand[: batchedDataCommand.index("_"):]
                if appService is not None:
                    requestParamsList = []
                    for dataItem in batchedDataValue:
                        requestData = dataItem["_request_data"]
                        requestParamsList.append(requestData["command_data"])
                    if commandMethod == "create":
                        appService.bulkCreate(objListParams=requestParamsList, token=metadataDict["token"])
                    elif commandMethod == "update":
                        appService.bulkUpdate(objListParams=requestParamsList, token=metadataDict["token"])
                    elif commandMethod == "delete":
                        appService.bulkDelete(objListParams=requestParamsList, token=metadataDict["token"])
                    elif commandMethod == "assign":
                        if entityName == 'permission_to_permission_context':
                            appService.bulkAssignPermissionToPermissionContext(
                                objListParams=requestParamsList, token=metadataDict["token"])
                        elif entityName == 'role_to_permission':
                            appService.bulkAssignRoleToPermission(
                                objListParams=requestParamsList, token=metadataDict["token"])
                    elif commandMethod == "remove":
                        if entityName == 'permission_to_permission_context_assignment':
                            appService.bulkRemovePermissionToPermissionContextAssignment(
                                objListParams=requestParamsList, token=metadataDict["token"])
            return {
                "name": self._commandConstant.value,
                "created_on": DateTimeHelper.utcNow(),
                "data": {"data": dataDict["data"], "total_item_count": totalItemCount},
                "metadata": metadataDict,
            }
        except ProcessBulkDomainException as e:
            return {
                "name": self._commandConstant.value,
                "created_on": DateTimeHelper.utcNow(),
                "data": {"data": dataDict["data"], "total_item_count": totalItemCount, "exceptions": e.extra},
                "metadata": metadataDict,
            }
        except DomainModelException as e:
            return {
                "name": self._commandConstant.value,
                "created_on": DateTimeHelper.utcNow(),
                "data": {
                    "data": dataDict["data"],
                    "total_item_count": totalItemCount,
                    "exceptions": [{"reason": {"message": e.message, "code": e.code}}],
                },
                "metadata": metadataDict,
            }

    def _sortKeyByCommand(self, item: dict):
        command = item['_request_data']['command']
        commandMethod = command[: command.index("_"):]
        switcher = {
            'create': 0,
            'update': 1,
            'assign': 2,
            'revoke': 3,
            'remove': 3,
            'delete': 4
        }
        return switcher.get(commandMethod, 5)

    def _batchSimilar(self, data):
        # The key will be the command like 'create_unit' and the value is the details of the command
        result = {}
        for item in data:
            command = item["_request_data"]["command"]
            if command not in result:
                result[command] = []
            result[command].append(item)
        return result

    def _appServiceByEntityName(self, entityName):
        entityToAppService = {
            # 'project': ProjectApplicationService,
            # 'role': RoleApplicationService,
            # 'user': UserApplicationService,
            "role_to_permission": PolicyApplicationService,
            "permission_to_permission_context": PolicyApplicationService,
            "permission_to_permission_context_assignment": PolicyApplicationService,
            "permission": PermissionApplicationService,
            "permission_context": PermissionContextApplicationService,
        }
        if entityName in entityToAppService:
            return AppDi.instance.get(entityToAppService[entityName])
        return None
