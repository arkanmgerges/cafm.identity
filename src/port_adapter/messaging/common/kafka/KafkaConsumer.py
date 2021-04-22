"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import json
import os
from typing import List, Any

from confluent_kafka import DeserializingConsumer as ConfluentKafkaConsumer
from confluent_kafka.serialization import StringDeserializer

from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset


class KafkaConsumer(Consumer):
    def __init__(
        self,
        groupId: str = "",
        autoCommit: bool = False,
        partitionEof: bool = True,
        autoOffsetReset: str = ConsumerOffsetReset.latest.name,
    ):
        self._consumer: ConfluentKafkaConsumer = ConfluentKafkaConsumer(
            {
                "bootstrap.servers": os.getenv("MESSAGE_BROKER_SERVERS", ""),
                "group.id": groupId,
                "auto.offset.reset": autoOffsetReset,
                "key.deserializer": StringDeserializer("utf_8"),
                "value.deserializer": lambda v, ctx: json.loads(v.decode("utf-8")),
                # Do not advance committed offsets outside of the transaction.
                # Consumer offsets are committed along with the transaction
                # using the producer's send_offsets_to_transaction() API.
                "enable.auto.commit": autoCommit,
                "enable.partition.eof": partitionEof,
            }
        )

    def poll(self, timeout: float = None) -> Any:
        return self._consumer.poll(timeout)

    def commit(self):
        self._consumer.commit()

    def close(self):
        self._consumer.close()

    def position(self, partitions: List[Any]) -> List[Any]:
        return self._consumer.position(partitions)

    def consumerGroupMetadata(self) -> Any:
        return self._consumer.consumer_group_metadata()

    def assignment(self) -> List[Any]:
        return self._consumer.assignment()

    def subscribe(self, topics: List[str]) -> None:
        self._consumer.subscribe(topics)

    def unsubscribe(self) -> None:
        self._consumer.unsubscribe()
