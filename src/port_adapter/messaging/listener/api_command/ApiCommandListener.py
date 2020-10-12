"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import os
import signal

from confluent_kafka.cimpl import KafkaError

import src.port_adapter.AppDi as AppDi
from src.domain_model.resource.exception.DomainModelException import DomainModelException
from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.port_adapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.port_adapter.messaging.common.model.ApiResponse import ApiResponse
from src.port_adapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.port_adapter.messaging.listener.api_command.handler.CreateRoleHandler import CreateRoleHandler
from src.port_adapter.messaging.listener.api_command.handler.CreateUserHandler import CreateUserHandler
from src.port_adapter.messaging.listener.api_command.handler.DeleteRoleHandler import DeleteRoleHandler
from src.port_adapter.messaging.listener.api_command.handler.UpdateRoleHandler import UpdateRoleHandler
from src.resource.logging.logger import logger


class ApiCommandListener:
    def __init__(self):
        self._handlers = []
        self._creatorServiceName = os.getenv('CAFM_IDENTITY_SERVICE_NAME', 'cafm.identity')
        self.addHandlers()
        signal.signal(signal.SIGINT, self.interruptExecution)
        signal.signal(signal.SIGTERM, self.interruptExecution)

    def interruptExecution(self, _signum, _frame):
        raise SystemExit()

    def run(self):
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=os.getenv('CAFM_IDENTITY_CONSUMER_GROUP_API_CMD_NAME', ''), autoCommit=False, partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name)

        # Subscribe
        consumer.subscribe([os.getenv('CAFM_API_COMMAND_TOPIC', '')])

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
                        logger.info(
                            f'[{ApiCommandListener.run.__qualname__}] - msg reached partition eof: {msg.error()}')
                    else:
                        logger.error(msg.error())
                else:
                    # Proper message
                    logger.info(
                        f'[{ApiCommandListener.run.__qualname__}] - topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()} with key: {str(msg.key())}')
                    logger.info(f'value: {msg.value()}')

                    try:
                        msgData = msg.value()
                        handledResult = self.handleCommand(name=msgData['name'], data=msgData['data'], metadata=msgData['metadata'])
                        if handledResult is None:  # Consume the offset since there is no handler for it
                            logger.info(
                                f'[{ApiCommandListener.run.__qualname__}] - Consume the offset for handleCommand(name={msgData["name"]}, data={msgData["data"]}, metadata={msgData["metadata"]})')
                            producer.sendOffsetsToTransaction(consumer)
                            producer.commitTransaction()
                            producer.beginTransaction()
                            continue

                        logger.debug(
                            f'[{ApiCommandListener.run.__qualname__}] - handleResult returned with: {handledResult}')
                        producer.produce(
                            obj=IdentityCommand(id=msgData['id'],
                                                creatorServiceName=self._creatorServiceName,
                                                name=msgData['name'],
                                                metadata=msgData['metadata'],
                                                data=json.dumps(handledResult['data']),
                                                createdOn=handledResult['createdOn'],
                                                externalId=msgData['id'],
                                                externalServiceName=msgData['creatorServiceName'],
                                                externalName=msgData['name'],
                                                externalMetadata=msgData['metadata'],
                                                externalData=msgData['data'],
                                                externalCreatedOn=msgData['createdOn']),
                            schema=IdentityCommand.get_schema())

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
                                            metadata=msgData['metadata'],
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
            logger.info(f'[{ApiCommandListener.run.__qualname__}] - Aborted by user')
        except SystemExit:
            logger.info(f'[{ApiCommandListener.run.__qualname__}] - Shutting down the process')
        finally:
            producer.abortTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()

    def handleCommand(self, name, data, metadata: str):
        for handler in self._handlers:
            if handler.canHandle(name):
                result = handler.handleCommand(name=name, data=data, metadata=metadata)
                return {"data": "", "metadata": metadata} if result is None else result
        return None

    def addHandlers(self):
        self._handlers.append(CreateUserHandler())
        self._handlers.append(CreateRoleHandler())
        self._handlers.append(DeleteRoleHandler())
        self._handlers.append(UpdateRoleHandler())


ApiCommandListener().run()
