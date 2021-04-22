"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os

from src.port_adapter.messaging.common.SimpleProducer import SimpleProducer
from src.resource.logging.logger import logger

MESSAGE_SCHEMA_REGISTRY_URL = os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")


class KafkaDeliveryReport(SimpleProducer):
    @classmethod
    def deliveryReport(cls, err, msg):
        """
        Reports the failure or success of a message delivery.

        Args:
            err (KafkaError): The error that occurred on None on success.

            msg (Message): The message that was produced or failed.

        Note:
            In the delivery report callback the Message.key() and Message.value()
            will be the binary format as encoded by any configured Serializers and
            not the same object that was passed to produce().
            If you wish to pass the original object(s) for key and value to delivery
            report callback we recommend a bound callback or lambda where you pass
            the objects along.

        """
        if err is not None:
            logger.error(f"Delivery failed for record {msg.key}: {err}")
            return
        logger.info(
            f"record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )
