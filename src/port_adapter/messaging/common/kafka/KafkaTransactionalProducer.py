"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import json
import os
from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.avro import CachedSchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

from src.port_adapter.messaging.common.kafka.KafkaDeliveryReport import KafkaDeliveryReport

from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.port_adapter.messaging.common.model.MessageBase import MessageBase
from src.resource.logging.logger import logger

MESSAGE_SCHEMA_REGISTRY_URL = os.getenv('MESSAGE_SCHEMA_REGISTRY_URL', '')


class KafkaTransactionalProducer(TransactionalProducer):
    def __init__(self, schemaRegistry=None, transactionalId=str(uuid4())):
        self._schemaRegistry = schemaRegistry
        self._deliveryReport = KafkaDeliveryReport.deliveryReport
        self._producer = SerializingProducer({
            'bootstrap.servers': os.getenv('MESSAGE_BROKER_SERVERS', ''),
            'transactional.id': transactionalId,
            'key.serializer': StringSerializer('utf_8'),
            'value.serializer': lambda v, ctx: json.dumps(v).encode('utf-8')
        })

    def initTransaction(self) -> None:
        logger.info(f'init transaction')
        self._producer.init_transactions()

    def beginTransaction(self) -> None:
        logger.info(f'begin transaction')
        self._producer.begin_transaction()

    def abortTransaction(self) -> None:
        logger.info(f'abort transaction')
        self._producer.abort_transaction()

    def commitTransaction(self) -> None:
        logger.info(f'commit transaction')
        self._producer.commit_transaction()

    def produce(self, obj: MessageBase, schema: dict):
        c = CachedSchemaRegistryClient({'url': MESSAGE_SCHEMA_REGISTRY_URL})
        res = c.test_compatibility(subject=f'{schema.namespace}.{schema.name}', avro_schema=schema)
        if not res:
            raise Exception(f'Schema is not compatible {schema}')

        keyId = obj.msgKey()
        logger.info(f'produce for id {keyId}')
        self._producer.poll(0.0)
        self._producer.produce(topic=obj.topic(), key=keyId, value=obj.toMap(),
                               on_delivery=self._deliveryReport)

    def sendOffsetsToTransaction(self, consumer: Consumer):
        logger.info(f'send offsets to transaction for consumer {consumer}')
        self._producer.send_offsets_to_transaction(consumer.position(consumer.assignment()),
                                                   consumer.consumerGroupMetadata())
