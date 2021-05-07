"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import os
from time import sleep

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.port_adapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.port_adapter.messaging.listener.common.CommonListener import CommonListener
from src.port_adapter.messaging.listener.common.ProcessHandleData import ProcessHandleData
from src.resource.logging.logger import logger


class IdentityFailedEventHandleListener(CommonListener):
    def __init__(self):
        super().__init__(
            creatorServiceName=os.getenv("CAFM_PROJECT_SERVICE_NAME", "cafm.identity"),
            handlersPath=f"{os.path.dirname(os.path.abspath(__file__))}/handler/**/*.py",
        )

    def run(self):
        self._process(
            consumerGroupId=os.getenv(
                "CAFM_IDENTITY_CONSUMER_GROUP_FAILED_EVT_HANDLE_NAME",
                "cafm.identity.consumer-group.failed-evt-handle",
            ),
            consumerTopicList=[os.getenv("CAFM_IDENTITY_FAILED_EVENT_HANDLE_TOPIC", "cafm.identity.failed-evt-handle")],
        )

    def _processHandledResult(self, processHandleData: ProcessHandleData):
        handledResult = processHandleData.handledResult
        messageData = processHandleData.messageData
        producer = processHandleData.producer
        isMessageProcessed = False
        while not isMessageProcessed:
            try:
                if handledResult is None:  # Consume the offset since there is no handler for it
                    logger.info(
                        f"[{IdentityFailedEventHandleListener.run.__qualname__}] Command handle result is None, "
                        f"The offset is consumed "
                        f'for handleCommand(name={messageData["name"]}, data={messageData["data"]}, '
                        f'metadata={messageData["metadata"]})'
                    )
                    return

                logger.debug(
                    f"[{IdentityFailedEventHandleListener.run.__qualname__}] handleResult returned with: {handledResult}"
                )

                # Produce to project command
                if "external" in messageData:
                    external = messageData["external"]
                else:
                    external = []

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
                producer.produce(
                    obj=IdentityCommand(
                        id=messageData["id"],
                        creatorServiceName=self._creatorServiceName,
                        name=handledResult["name"],
                        metadata=messageData["metadata"],
                        data=json.dumps(handledResult["data"]),
                        createdOn=handledResult["created_on"],
                        external=external,
                    ),
                    schema=IdentityCommand.get_schema(),
                )

                processHandleData.isSuccess = True
                isMessageProcessed = True
            except DomainModelException as e:
                logger.warn(e)
                processHandleData.isSuccess = False
                processHandleData.exception = e
                DomainPublishedEvents.cleanup()
                isMessageProcessed = True
            except Exception as e:
                DomainPublishedEvents.cleanup()
                logger.error(e)
                sleep(1)

    def _processHandleCommand(self, processHandleData: ProcessHandleData):
        isMessageProcessed = False
        while not isMessageProcessed:
            try:
                return super()._handleCommand(processHandleData=processHandleData)
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


IdentityFailedEventHandleListener().run()