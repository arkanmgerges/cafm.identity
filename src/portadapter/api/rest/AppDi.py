from uuid import uuid4

from injector import Module, Injector, singleton, provider, inject

from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.portadapter.messaging.common.SimpleProducer import SimpleProducer
from src.portadapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.portadapter.messaging.common.kafka.KafkaConsumer import KafkaConsumer
from src.portadapter.messaging.common.kafka.KafkaProducer import KafkaProducer
from injector import ClassAssistedBuilder


class AppDi(Module):
    """
    Dependency injection module of the app

    """

    @singleton
    @provider
    def provideSimpleProducer(self) -> SimpleProducer:
        return KafkaProducer.simpleProducer()

    @singleton
    @provider
    def provideTransactionalProducer(self) -> TransactionalProducer:
        return KafkaProducer.transactionalProducer()

    @singleton
    @provider
    def provideConsumer(self, groupId: str = uuid4(), autoCommit: bool = False,
                        partitionEof: bool = True, autoOffsetReset: str = ConsumerOffsetReset.earliest.name) -> Consumer:
        return KafkaConsumer(groupId=groupId, autoCommit=autoCommit, partitionEof=partitionEof,
                             autoOffsetReset=autoOffsetReset)


class Builder:
    @classmethod
    def buildConsumer(cls, groupId: str = uuid4(), autoCommit: bool = False,
                      partitionEof: bool = True, autoOffsetReset: str = ConsumerOffsetReset.earliest.name) -> Consumer:
        builder = instance.get(ClassAssistedBuilder[KafkaConsumer])
        return builder.build(groupId=groupId, autoCommit=autoCommit, partitionEof=partitionEof,
                             autoOffsetReset=autoOffsetReset)


instance = Injector([AppDi])
