"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os
import signal
import traceback

from confluent_kafka.cimpl import KafkaError

import src.portadapter.AppDi as AppDi
from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.portadapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.portadapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.portadapter.messaging.listener.handler.CreateUserHandler import CreateUserHandler
from src.resource.logging.logger import logger


class ApiCommandListener:
    def __init__(self):
        self._handlers = []
        self.addHandlers()
        signal.signal(signal.SIGINT, self.interruptExecution)
        signal.signal(signal.SIGTERM, self.interruptExecution)

    def interruptExecution(self, _signum, _frame):
        raise SystemExit()

    def run(self):
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=os.getenv('CORAL_IDENTITY_CONSUMER_GROUP_API_CMD_NAME', ''), autoCommit=False, partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name)

        # Subscribe
        consumer.subscribe([os.getenv('CORAL_API_COMMAND_TOPIC', '')])

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

                        producer.produce(
                            obj=IdentityCommand(id=msgData['id'],
                                                serviceName='coral.identity',
                                                name=handledResult['name'],
                                                data=handledResult['data'],
                                                createdOn=handledResult['createdOn'],
                                                externalId=msgData['id'],
                                                externalServiceName=msgData['creatorServiceName'],
                                                externalName=msgData['name'],
                                                externalData=msgData['data'],
                                                externalCreatedOn=msgData['createdOn']),
                            schema=IdentityCommand.get_schema())

                        # Send the consumer's position to transaction to commit
                        # them along with the transaction, committing both
                        # input and outputs in the same transaction is what provides EOS.
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
            # Close down consumer to commit final offsets.
            consumer.close()

    def handleCommand(self, name, data):
        for handler in self._handlers:
            if handler.canHandle(name):
                return handler.handleCommand(name=name, data=data)

    def addHandlers(self):
        self._handlers.append(CreateUserHandler())


ApiCommandListener().run()
