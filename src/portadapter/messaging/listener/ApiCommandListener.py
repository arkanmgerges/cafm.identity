"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os
from time import sleep

from confluent_kafka.cimpl import KafkaError

import src.portadapter.api.rest.AppDi as AppDi
from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.resource.logging.logger import logger


class ApiCommandListener:

    @staticmethod
    def run():
        consumer: Consumer = AppDi.Builder.buildConsumer(
            groupId=os.getenv('CORAL_IDENTITY_CONSUMER_GROUP_API_CMD_NAME', ''), autoCommit=False, partitionEof=True,
            autoOffsetReset=ConsumerOffsetReset.earliest.name)

        # Subscribe
        consumer.subscribe([os.getenv('CORAL_API_COMMAND_TOPIC', '')])
        try:
            while True:
                try:
                    msg = consumer.poll(timeout=1.0)
                except Exception as _e:
                    pass
                if msg is None:
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
                sleep(3)
        except KeyboardInterrupt:
            logger.info(f'Aborted by user')
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()


ApiCommandListener.run()
