import json
import os
from base64 import b64encode
from time import sleep

from confluent_kafka.cimpl import KafkaError

import src.portadapter.api.rest.AppDi as AppDi
from src.portadapter.messaging.common.Consumer import Consumer
from injector import ClassAssistedBuilder
from src.resource.logging.logger import logger
from src.portadapter.messaging.common.kafka.KafkaConsumer import KafkaOffsetReset, KafkaConsumer


class CommandApiListener:

    @classmethod
    def processInput(msg):
        """
        Base64 encodes msg key/value contents
        :param msg:
        :returns: transformed key, value
        :rtype: tuple
        """

        key, value = None, None
        if msg.key() is not None:
            key = b64encode(msg.key())
        if msg.value() is not None:
            value = b64encode(msg.value())

        return key, value

    @staticmethod
    def run():
        instance = AppDi.instance
        builder = instance.get(ClassAssistedBuilder[KafkaConsumer])
        consumer: Consumer = builder.build(groupId=os.getenv('CORAL_API_CONSUMER_GROUP_CMD_NAME', ''), autoCommit=False, partitionEof=True, autoOffsetReset=KafkaOffsetReset.earliest.name)

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
                    logger.info(f'topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()} with key: {str(msg.key())}')
                    logger.info(f'value: {msg.value()}')
                sleep(3)
        except KeyboardInterrupt:
            logger.info(f'Aborted by user')
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()


CommandApiListener.run()
