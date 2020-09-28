"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os

from confluent_kafka.cimpl import KafkaError

import src.portadapter.AppDi as AppDi
from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.portadapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.portadapter.messaging.common.model.IdentityCommand import IdentityCommand
from src.resource.logging.logger import logger


class ApiCommandListener:

    @staticmethod
    def run():
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
                        producer.produce(
                            obj=IdentityCommand(id=msgData['id'],
                                                serviceName=msgData['creatorServiceName'],
                                                name=msgData['name'],
                                                data=msgData['data'],
                                                createdOn=msgData['createdOn'],
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
        finally:
            producer.commitTransaction()
            # Close down consumer to commit final offsets.
            consumer.close()


ApiCommandListener.run()
