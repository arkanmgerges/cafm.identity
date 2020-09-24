from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient, record_subject_name_strategy
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

from src.resource.logging.logger import logger

import os

from src.portadapter.messaging.Producer import Producer

MESSAGE_SCHEMA_REGISTRY_URL = os.environ.get('MESSAGE_SCHEMA_REGISTRY_URL', '')


class KafkaProducer(Producer):
    def __init__(self):
        self._schemaRegistry = SchemaRegistryClient({'url': MESSAGE_SCHEMA_REGISTRY_URL})

    def _deliveryReport(self, err, msg):
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
            logger.error(f'Delivery failed for record {msg.key}: {err}')
            return
        logger.info(
            f'record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

    def simpleProducer(self, obj: object, objMap: callable, schema: str):
        """Send message to the message broker

        Args:
            obj (object): The object model that is needed to be sent
            objMap (callable): A function that will be called by the system in order to get a json representation for
            the data to be sent
            schema (str): The schema that will be used for data validation

        """
        brokers = os.environ.get('MESSAGE_BROKER_SERVERS', '')
        topic = os.environ.get('CORAL_API_COMMAND_TOPIC', '')
        try:
            avroSerializer = AvroSerializer(
                schema,
                self._schemaRegistry,
                objMap,
                conf={'subject.name.strategy': record_subject_name_strategy,
                      'auto.register.schemas': False}
            )
            producerConf = {'bootstrap.servers': brokers,
                            'key.serializer': StringSerializer('utf_8'),
                            'value.serializer': avroSerializer}
            return SerializingProducer(producerConf)
            # producer = SerializingProducer(producerConf)
            # producer.poll(0.0)
            # producer.produce(topic=topic, key=str(uuid4()), value=obj,
            #                  on_delivery=self._deliveryReport)
            # producer.flush()
        except Exception as e:
            logger.error(e)

    def transactionalProducer(self, obj: object, objMap: callable, schema: str, transactionalId: str = ''):
        """Send message to the message broker using a transactional id

        Args:
            obj (object): The object model that is needed to be sent
            objMap (callable): A function that will be called by the system in order to get a json representation for
            the data to be sent
            schema (str): The schema that will be used for data validation
            transactionalId (str): This is the transactional id used in message broker transaction

        """
        brokers = os.environ.get('MESSAGE_BROKER_SERVERS', '')
        topic = os.environ.get('CORAL_API_COMMAND_TOPIC', '')
        try:
            avroSerializer = AvroSerializer(
                schema,
                self._schemaRegistry,
                objMap,
                conf={'subject.name.strategy': record_subject_name_strategy,
                      'auto.register.schemas': False}
            )
            producerConf = {'bootstrap.servers': brokers,
                            'key.serializer': StringSerializer('utf_8'),
                            'value.serializer': avroSerializer,
                            'transactional.id': transactionalId}
            return SerializingProducer(producerConf)
            # producer = SerializingProducer(producerConf)
            # producer.poll(0.0)
            # producer.produce(topic=topic, key=str(uuid4()), value=obj,
            #                  on_delivery=self._deliveryReport)
            # producer.flush()
        except Exception as e:
            logger.error(e)
