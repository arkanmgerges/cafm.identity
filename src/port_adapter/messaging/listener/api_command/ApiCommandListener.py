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
from src.port_adapter.messaging.common.model.ApiCommand import ApiCommand
from src.port_adapter.messaging.common.model.ApiFailedCommandHandle import ApiFailedCommandHandle
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.CommonListener import CommonListener
from src.port_adapter.messaging.listener.common.ProcessHandleData import ProcessHandleData
from src.port_adapter.messaging.listener.common.resource.exception.FailedMessageHandleException import \
    FailedMessageHandleException
from src.resource.logging.logger import logger


class ApiCommandListener(CommonListener):
    def __init__(self):
        super().__init__(
            creatorServiceName=os.getenv("CAFM_IDENTITY_SERVICE_NAME", "cafm.identity"),
            handlersPath=f"{os.path.dirname(os.path.abspath(__file__))}/handler/**/*.py",
        )

    def run(self):
        self._process(
            consumerGroupId=os.getenv("CAFM_IDENTITY_CONSUMER_GROUP_API_CMD_NAME", "cafm.identity.consumer-group.api.cmd"),
            consumerTopicList=[os.getenv("CAFM_API_COMMAND_TOPIC", "cafm.api.cmd")],
        )

    def _processHandledResult(self, processHandleData: ProcessHandleData):
        handledResult = processHandleData.handledResult
        messageData = processHandleData.messageData
        producer = processHandleData.producer
        try:
            if handledResult is None:  # Consume the offset since there is no handler for it
                logger.info(
                    f'[{ApiCommandListener.run.__qualname__}] Command handle result is None, The offset is consumed for handleCommand(name={messageData["name"]}, data={messageData["data"]}, metadata={messageData["metadata"]})'
                )
                return

            logger.debug(f"[{ApiCommandListener.run.__qualname__}] handleResult returned with: {handledResult}")
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

            # Produce the domain events
            logger.debug(f"[{ApiCommandListener.run.__qualname__}] get postponed events from the event publisher")
            domainEvents = DomainPublishedEvents.postponedEvents()

            # Exclude the external data when it is a bulk, this will avoid adding the bulk data for each
            # event in the messaging system
            evtExternal = []
            if (
                    len(external) > 0
                    and "name" in external[0]
                    and external[0]["name"] != CommonCommandConstant.PROCESS_BULK.value
            ):
                evtExternal = external

            for domainEvent in domainEvents:
                logger.debug(
                    f"[{ApiCommandListener.run.__qualname__}] produce domain event with name = {domainEvent.name()}"
                )
                producer.produce(
                    obj=IdentityEvent(
                        id=domainEvent.id(),
                        creatorServiceName=self._creatorServiceName,
                        name=domainEvent.name(),
                        metadata=messageData["metadata"],
                        data=json.dumps(domainEvent.data()),
                        createdOn=domainEvent.occurredOn(),
                        external=evtExternal,
                    ),
                    schema=IdentityEvent.get_schema(),
                )

            logger.debug(f"[{ApiCommandListener.run.__qualname__}] cleanup event publisher")
            processHandleData.isSuccess = True
            DomainPublishedEvents.cleanup()

        except DomainModelException as e:
            logger.warn(e)
            DomainPublishedEvents.cleanup()
            processHandleData.exception = e
            processHandleData.isSuccess = False

        except Exception as e:
            # Send the failed message to the failed topic
            DomainPublishedEvents.cleanup()
            isMessageProduced = False
            logger.error(e)
            while not isMessageProduced:
                try:
                    self._produceToFailedTopic(processHandleData=processHandleData)
                    isMessageProduced = True
                except Exception as e:
                    logger.error(e)
                    sleep(1)
            raise FailedMessageHandleException(message=f"Failed message: {processHandleData.messageData}")

    def _processHandleCommand(self, processHandleData: ProcessHandleData):
        try:
            # Sometimes we are modifying messageData['data'], e.g. on update we are using 'new' and overwrite
            # messageData['data'], that is why we need to send a copy
            processHandleDataCopy = copy(processHandleData)
            processHandleDataCopy.messageData = copy(processHandleData.messageData)
            return super()._handleCommand(processHandleData=processHandleDataCopy)
        except DomainModelException as e:
            logger.warn(e)
            DomainPublishedEvents.cleanup()
            processHandleData.exception = e
            processHandleData.isSuccess = False
        except Exception as e:
            # Send the failed message to the failed topic
            DomainPublishedEvents.cleanup()
            isMessageProduced = False
            logger.error(e)
            while not isMessageProduced:
                try:
                    self._produceToFailedTopic(processHandleData=processHandleData)
                    isMessageProduced = True
                except Exception as e:
                    logger.error(e)
                    sleep(1)
            raise FailedMessageHandleException(message=f"Failed message: {processHandleData.messageData}")

    def _produceToFailedTopic(self, processHandleData: ProcessHandleData):
        messageData = processHandleData.messageData
        producer = processHandleData.producer
        consumer = processHandleData.consumer

        producer.produce(
            obj=ApiFailedCommandHandle(
                id=messageData["id"],
                creatorServiceName=self._creatorServiceName,
                name=messageData["name"],
                metadata=messageData["metadata"],
                data=messageData["data"],
                createdOn=messageData["created_on"],
            ),
            schema=ApiCommand.get_schema(),
        )
        producer.sendOffsetsToTransaction(consumer)
        producer.commitTransaction()
        producer.beginTransaction()


ApiCommandListener().run()
