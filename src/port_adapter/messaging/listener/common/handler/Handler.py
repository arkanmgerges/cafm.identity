"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from _ctypes_test import func
from abc import ABC, abstractmethod
from typing import List

from src.port_adapter.messaging.common.model.ApiResponse import ApiResponse


class Handler(ABC):
    @abstractmethod
    def canHandle(self, name: str) -> bool:
        """Can handle the command

        Args:
            name (str): The command name

        Returns:
            bool: Returns True if it can handle the command, False otherwise
        """

    @abstractmethod
    def handleCommand(self, messageData: dict) -> dict:
        """Handle the command

        Args:
            messageData (dict): The associated data for the command to handle

        Returns:
            dict: The result of the handler
        """

    @staticmethod
    def targetsOnSuccess() -> List[func]:
        """Returns the targets that need to be contacted on success
        Returns:
            List[function]: It's a dictionary that has the keys 'obj' and 'schema'
        """
        return []

    @staticmethod
    def targetsOnException() -> List[func]:
        """Returns the targets that need to be contacted on exception

        Returns:
            List[function]: It's a dictionary that has the keys 'obj' and 'schema'
        """
        return [Handler.targetOnException]

    @staticmethod
    def targetOnException(messageData: dict, e: Exception, creatorServiceName: str) -> dict:
        external = messageData['external']
        dataDict = external[0] if len(external) > 0 else messageData
        return {'obj': ApiResponse(commandId=dataDict['id'], commandName=dataDict['name'],
                                   metadata=messageData['metadata'],
                                   data=json.dumps({'reason': {'message': e.message, 'code': e.code}}),
                                   creatorServiceName=creatorServiceName, success=False),
                'schema': ApiResponse.get_schema()
                }

    @staticmethod
    def targetOnSuccess(messageData: dict, creatorServiceName: str, resultData: dict) -> dict:
        external = messageData['external']
        dataDict = external[0] if len(external) > 0 else messageData
        return {'obj': ApiResponse(commandId=dataDict['id'], commandName=dataDict['name'],
                                   metadata=messageData['metadata'],
                                   data=json.dumps(resultData),
                                   creatorServiceName=creatorServiceName, success=True),
                'schema': ApiResponse.get_schema()}
