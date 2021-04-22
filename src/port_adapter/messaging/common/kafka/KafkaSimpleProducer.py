"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import json
import os
from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.avro import CachedSchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

from src.port_adapter.messaging.common.SimpleProducer import SimpleProducer
from src.port_adapter.messaging.common.kafka.KafkaDeliveryReport import (
    KafkaDeliveryReport,
)
from src.port_adapter.messaging.common.model.MessageBase import MessageBase

MESSAGE_SCHEMA_REGISTRY_URL = os.getenv("MESSAGE_SCHEMA_REGISTRY_URL", "")


class KafkaSimpleProducer(SimpleProducer):
    def __init__(self, schemaRegistry=None):
        self._schemaRegistry = schemaRegistry
        self._deliveryReport = KafkaDeliveryReport.deliveryReport

    def produce(self, obj: MessageBase, schema: dict):
        c = CachedSchemaRegistryClient({"url": MESSAGE_SCHEMA_REGISTRY_URL})
        res = c.test_compatibility(
            subject=f"{schema.namespace}.{schema.name}", avro_schema=schema
        )
        if not res:
            raise Exception(f"Schema is not compatible {schema}")

        producerConf = {
            "bootstrap.servers": os.getenv("MESSAGE_BROKER_SERVERS", ""),
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": lambda v, ctx: json.dumps(v).encode("utf-8"),
        }
        producer = SerializingProducer(producerConf)
        producer.poll(0.0)
        producer.produce(
            topic=obj.topic(),
            key=obj.msgKey(),
            value=obj.toMap(),
            on_delivery=self._deliveryReport,
        )
        producer.flush()
