import json
import os
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.avro import CachedSchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

from src.portadapter.messaging.common.kafka.KafkaDeliveryReport import KafkaDeliveryReport

from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.portadapter.messaging.common.model.MessageBase import MessageBase

MESSAGE_SCHEMA_REGISTRY_URL = os.getenv('MESSAGE_SCHEMA_REGISTRY_URL', '')


class KafkaTransactionalProducer(TransactionalProducer):
    def __init__(self, schemaRegistry=None, transactionalId=str(uuid4())):
        self._schemaRegistry = schemaRegistry
        self._deliveryReport = KafkaDeliveryReport.deliveryReport
        self._producer = Producer({
            'bootstrap.servers': os.getenv('MESSAGE_BROKER_SERVERS', ''),
            'key.serializer': StringSerializer('utf_8'),
            'value.serializer': lambda v, ctx: json.dumps(v).encode('utf-8')
        })

    def initTransaction(self) -> None:
        self._producer.initTransaction()

    def beginTransaction(self) -> None:
        self._producer.beginTransaction()

    def abortTransaction(self) -> None:
        self._producer.abortTransaction()

    def commitTransaction(self) -> None:
        self._producer.commitTransaction()

    def produce(self, obj: MessageBase, schema: dict):
        c = CachedSchemaRegistryClient({'url': MESSAGE_SCHEMA_REGISTRY_URL})
        res = c.test_compatibility(subject=f'{schema.namespace}.{schema.name}', avro_schema=schema)
        if not res:
            raise Exception(f'Schema is not compatible {schema}')

        self._producer.poll(0.0)
        self._producer.produce(topic=obj.topic(), key=str(uuid4()), value=obj.toMap(),
                         on_delivery=self._deliveryReport)

    def sendOffsetsToTransaction(self, consumer: Consumer):
        self._producer.send_offsets_to_transaction(consumer.position(consumer.assignment()),
                                                   consumer.consumerGroupMetadata())

