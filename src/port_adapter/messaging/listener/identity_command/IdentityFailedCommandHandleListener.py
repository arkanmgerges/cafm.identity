"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import os
from copy import copy
from time import sleep

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.CommonListener import CommonListener
from src.port_adapter.messaging.listener.common.ProcessHandleData import ProcessHandleData
from src.resource.logging.logger import logger


class IdentityFailedCommandHandleListener(CommonListener):
    def __init__(self):
        super().__init__(
            creatorServiceName=os.getenv("CAFM_IDENTITY_SERVICE_NAME", "cafm.identity"),
            handlersPath=f"{os.path.dirname(os.path.abspath(__file__))}/handler/**/*.py",
        )

    def run(self):
        self._process(
            consumerGroupId=os.getenv(
                "CAFM_IDENTITY_CONSUMER_GROUP_FAILED_CMD_HANDLE_NAME", "cafm.identity.consumer-group.failed-cmd-handle"
            ),
            consumerTopicList=[
                os.getenv("CAFM_IDENTITY_FAILED_COMMAND_HANDLE_TOPIC", "cafm.identity.failed-cmd-handle")
            ],
        )

    def _processHandledResult(self, processHandleData: ProcessHandleData):
        handledResult = processHandleData.handledResult
        messageData = processHandleData.messageData
        producer = processHandleData.producer
        isMessageProcessed = False
        while not isMessageProcessed:
            try:
                external = []
                if "external" in messageData:
                    external = messageData["external"]

                external.append(
                    {
                        "id": messageData["id"],
                        "creator_service_name": messageData["creator_service_name"],
                        "name": messageData["name"],
                        "version": messageData["version"],
                        "metadata": messageData["metadata"],
                        "data": messageData["data"],
                        "created_on": messageData["created_on"],
                    }
                )

                # Exclude the external data when it is a bulk, this will avoid adding the bulk data for each
                # event in the messaging system
                evtExternal = []
                if (
                    len(external) > 0
                    and "name" in external[0]
                    and external[0]["name"] != CommonCommandConstant.PROCESS_BULK.value
                ):
                    evtExternal = external

                if handledResult is None:  # Consume the offset since there is no handler for it
                    logger.info(
                        f"[{IdentityFailedCommandHandleListener.run.__qualname__}] Command handle result is None, The "
                        f'offset is consumed for handleMessage(name={messageData["name"]}, data='
                        f'{messageData["data"]}, metadata={messageData["metadata"]})'
                    )
                    self._produceDomainEvents(producer=producer, messageData=messageData, external=evtExternal)
                    return

                logger.debug(
                    f"[{IdentityFailedCommandHandleListener.run.__qualname__}] handleResult "
                    f"returned with: {handledResult}"
                )

                self._produceDomainEvents(producer=producer, messageData=messageData, external=evtExternal)
                processHandleData.isSuccess = True
                isMessageProcessed = True

            except DomainModelException as e:
                logger.warn(e)
                DomainPublishedEvents.cleanup()
                processHandleData.exception = e
                processHandleData.isSuccess = False
                isMessageProcessed = True
            except Exception as e:
                DomainPublishedEvents.cleanup()
                logger.error(e)
                sleep(1)

    def _processHandleMessage(self, processHandleData: ProcessHandleData):
        isMessageProcessed = False
        while not isMessageProcessed:
            try:
                # Sometimes we are modifying messageData['data'], e.g. on update we are using 'new' and overwrite
                # messageData['data'], that is why we need to send a copy
                processHandleDataCopy = copy(processHandleData)
                processHandleDataCopy.messageData = copy(processHandleData.messageData)
                return super()._handleMessage(processHandleData=processHandleDataCopy)
            except DomainModelException as e:
                logger.warn(e)
                DomainPublishedEvents.cleanup()
                processHandleData.exception = e
                processHandleData.isSuccess = False
                isMessageProcessed = True
            except Exception as e:
                # Send the failed message to the failed topic
                DomainPublishedEvents.cleanup()
                logger.error(e)
                sleep(1)


IdentityFailedCommandHandleListener().run()
