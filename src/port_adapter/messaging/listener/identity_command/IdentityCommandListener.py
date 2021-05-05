"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import os

from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.domain_model.resource.exception.DomainModelException import (
    DomainModelException,
)
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.CommonListener import CommonListener
from src.resource.logging.logger import logger


class IdentityCommandListener(CommonListener):
    def __init__(self):
        super().__init__(
            creatorServiceName=os.getenv("CAFM_IDENTITY_SERVICE_NAME", "cafm.identity"),
            handlersPath=f"{os.path.dirname(os.path.abspath(__file__))}/handler/**/*.py",
        )

    def run(self):
        self._process(
            consumerGroupId=os.getenv("CAFM_IDENTITY_CONSUMER_GROUP_IDENTITY_CMD_NAME", ""),
            consumerTopicList=[os.getenv("CAFM_IDENTITY_COMMAND_TOPIC", "")],
        )

    def _processHandledResult(self, producer, consumer, handledResult, messageData):
        try:
            if handledResult is None:  # Consume the offset since there is no handler for it
                logger.info(
                    f'[{IdentityCommandListener.run.__qualname__}] Command handle result is None, The offset is consumed for handleCommand(name={messageData["name"]}, data={messageData["data"]}, metadata={messageData["metadata"]})'
                )
                return

            logger.debug(f"[{IdentityCommandListener.run.__qualname__}] handleResult returned with: {handledResult}")
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

            for target in self.targetsOnSuccess:
                res = target(
                    messageData=messageData,
                    creatorServiceName=self._creatorServiceName,
                    resultData=handledResult["data"],
                )
                producer.produce(obj=res["obj"], schema=res["schema"])

            # Produce the domain events
            logger.debug(f"[{IdentityCommandListener.run.__qualname__}] get postponed events from the event publisher")
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
                    f"[{IdentityCommandListener.run.__qualname__}] produce domain event with name = {domainEvent.name()}"
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

            logger.debug(f"[{IdentityCommandListener.run.__qualname__}] cleanup event publisher")
            DomainPublishedEvents.cleanup()

        except DomainModelException as e:
            logger.warn(e)
            for target in self.targetsOnException:
                res = target(messageData, e, self._creatorServiceName)
                producer.produce(obj=res["obj"], schema=res["schema"])
            DomainPublishedEvents.cleanup()

        except Exception as e:
            DomainPublishedEvents.cleanup()
            # todo send to delayed topic and make isMessageProcessed = True
            logger.error(e)
            raise e


IdentityCommandListener().run()
