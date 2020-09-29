"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import os

from confluent_kafka.schema_registry import SchemaRegistryClient

from src.port_adapter.messaging.common.kafka.KafkaSimpleProducer import KafkaSimpleProducer
from src.port_adapter.messaging.common.kafka.KafkaTransactionalProducer import KafkaTransactionalProducer

MESSAGE_SCHEMA_REGISTRY_URL = os.getenv('MESSAGE_SCHEMA_REGISTRY_URL', '')


class KafkaProducer:
    @classmethod
    def simpleProducer(cls):
        """Producer that is simply used to send one message, no transaction is handled using this producer

        Returns:
            `SimpleProducer <src.port_adapter.messaging.SimpleProducer>`: SimpleProducer base class
        """
        return KafkaSimpleProducer(schemaRegistry=SchemaRegistryClient({'url': MESSAGE_SCHEMA_REGISTRY_URL}))

    @classmethod
    def transactionalProducer(cls):
        """Producer that is using transaction in order to persist the messages with the provided consumers

            Returns:
            `TransactionalProducer <src.port_adapter.messaging.TransactionalProducer>`: TransactionalProducer base class
        """
        return KafkaTransactionalProducer(schemaRegistry=SchemaRegistryClient({'url': MESSAGE_SCHEMA_REGISTRY_URL}))
