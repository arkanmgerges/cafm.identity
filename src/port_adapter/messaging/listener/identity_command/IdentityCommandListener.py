"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import os
import signal

from confluent_kafka.cimpl import KafkaError

import src.port_adapter.AppDi as AppDi
from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.port_adapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.port_adapter.messaging.common.model.ApiResponse import ApiResponse
from src.port_adapter.messaging.common.model.IdentityEvent import IdentityEvent
from src.port_adapter.messaging.listener.identity_command.handler.CreateUserHandler import CreateUserHandler
from src.resource.logging.logger import logger


class IdentityCommandListener:
    def __init__(self):
        self._handlers = []
        self._creatorServiceName = os.getenv('CORAL_IDENTITY_SERVICE_NAME', 'coral.identity')
        self._coralApiServiceName = os.getenv('CORAL_API_SERVICE_NAME', 'coral.api')
        self.addHandlers()
        signal.signal(signal.SIGINT, self.interruptExecution)
        signal.signal(signal.SIGTERM, self.interruptExecution)

    def interruptExecution(self, _signum, _frame):
        raise SystemExit()

    def run(self):
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=os.getenv('CORAL_IDENTITY_CONSUMER_GROUP_IDENTITY_CMD_NAME', ''), autoCommit=False,
            partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name)

        # Subscribe - Consume the commands that exist in this service own topic
        consumer.subscribe([os.getenv('CORAL_IDENTITY_COMMAND_TOPIC', '')])

        # Producer
        producer: TransactionalProducer = AppDi.instance.get(TransactionalProducer)
        producer.initTransaction()
        producer.beginTransaction()

        try:
            while True:
                try:
                    msg = consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                except Exception as _e:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(f'msg reached partition eof: {msg.error()}')
                    else:
                        logger.error(msg.error())
                else:
                    # Proper message
                    logger.info(
                        f'topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()} with key: {str(msg.key())}')
                    logger.info(f'value: {msg.value()}')

                    try:
                        msgData = msg.value()
                        handledResult = self.handleCommand(name=msgData['name'], data=msgData['data'])
                        logger.debug(f'handleResult returned with: {handledResult}')

                        # If the external service name who initiated the command is coral api service name, then
                        if msgData['externalServiceName'] == self._coralApiServiceName:
                            # Produce to api response
                            producer.produce(
                                obj=ApiResponse(commandId=msgData['externalId'], commandName=msgData['externalName'],
                                                data=json.dumps(handledResult['data']),
                                                creatorServiceName=self._creatorServiceName, success=True),
                                schema=ApiResponse.get_schema())

                        # Produce the domain events
                        logger.debug(
                            f'[{IdentityCommandListener.run.__qualname__}] - get postponed events from the event publisher')
                        domainEvents = DomainEventPublisher.postponedEvents()
                        for domainEvent in domainEvents:
                            logger.debug(
                                f'[{IdentityCommandListener.run.__qualname__}] - produce domain event with name = {domainEvent.name()}')
                            producer.produce(
                                obj=IdentityEvent(id=domainEvent.id(),
                                                  creatorServiceName=self._creatorServiceName,
                                                  name=domainEvent.name(),
                                                  data=json.dumps(domainEvent.data()),
                                                  occurredOn=domainEvent.occurredOn()),
                                schema=IdentityEvent.get_schema())

                        logger.debug(f'[{IdentityCommandListener.run.__qualname__}] - cleanup event publisher')
                        DomainEventPublisher.cleanup()
                        # Send the consumer's position to transaction to commit
                        # them along with the transaction, committing both
                        # input and outputs in the same transaction is what provides EOS.
                        producer.sendOffsetsToTransaction(consumer)
                        producer.commitTransaction()

                        producer.beginTransaction()
                    except DomainModelException as e:
                        logger.warn(e)
                        msgData = msg.value()
                        producer.produce(
                            obj=ApiResponse(commandId=msgData['id'], commandName=msgData['name'],
                                            data=json.dumps({'reason': {'message': e.message, 'code': e.code}}),
                                            creatorServiceName=self._creatorServiceName, success=False),
                            schema=ApiResponse.get_schema())
                        producer.sendOffsetsToTransaction(consumer)
                        producer.commitTransaction()
                        producer.beginTransaction()
                    except Exception as e:
                        logger.error(e)

                # sleep(3)
        except KeyboardInterrupt:
            logger.info(f'Aborted by user')
        except SystemExit:
            logger.info(f'Shutting down the process')
        finally:
            producer.abortTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()

    def handleCommand(self, name, data):
        for handler in self._handlers:
            if handler.canHandle(name):
                return handler.handleCommand(name=name, data=data)

    def addHandlers(self):
        self._handlers.append(CreateUserHandler())


IdentityCommandListener().run()
