"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from time import sleep

from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class ProcessBulkHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.PROCESS_BULK
        self._handlers = []

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict, extraData: dict = None) -> dict:
        data = messageData["data"]
        metadata = messageData["metadata"]

        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        # The is the final result of all the data items in the dataDict["data"]
        resultList = []
        handlers = extraData["handlers"]
        # Get the data item from the 'data' key
        for dataItem in dataDict["data"]:
            # Test each handler if it can handle the command
            for handler in handlers:
                requestData = dataItem["_request_data"]
                # Exclude the current handler from the handler list
                if not handler.canHandle(
                    CommonCommandConstant.PROCESS_BULK.value
                ) and handler.canHandle(requestData["command"]):
                    resultList.append(self.handleData(dataItem, handler, metadata))

        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": resultList,
            "metadata": metadataDict,
        }

    def handleData(self, dataItem, handler, metadata):
        requestData = dataItem["_request_data"]
        command = requestData["command"]
        commandData = requestData["command_data"]
        loop = True
        while loop:
            try:
                # Handle the command
                result = handler.handleCommand(
                    messageData={
                        "name": command,
                        "data": json.dumps(commandData),
                        "metadata": metadata,
                    }
                )
                dataItem["result"] = result
                return dataItem
            except DomainModelException as e:
                # Add the reason for the failure
                result = {"reason": {"message": e.message, "code": e.code}}
                dataItem["result"] = result
                return dataItem
            except Exception as e:
                # Loop continuously and print the error
                logger.error(e)
                sleep(2)
