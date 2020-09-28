from uuid import uuid4

from injector import Module, Injector, singleton, provider, inject

from src.application.RoleApplicationService import RoleApplicationService
from src.application.UserApplicationService import UserApplicationService
from src.domainmodel.role.RoleRepository import RoleRepository
from src.domainmodel.user.UserRepository import UserRepository
from src.portadapter.messaging.common.Consumer import Consumer
from src.portadapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.portadapter.messaging.common.SimpleProducer import SimpleProducer
from src.portadapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.portadapter.messaging.common.kafka.KafkaConsumer import KafkaConsumer
from src.portadapter.messaging.common.kafka.KafkaProducer import KafkaProducer
from injector import ClassAssistedBuilder

from src.portadapter.repository.arangodb.role.RoleRepositoryImpl import RoleRepositoryImpl
from src.portadapter.repository.arangodb.user.UserRepositoryImpl import UserRepositoryImpl


class AppDi(Module):
    """
    Dependency injection module of the app

    """

    # region Application service
    @singleton
    @provider
    def provideUserApplicationService(self) -> UserApplicationService:
        return UserApplicationService(self.__injector__.get(UserRepository))
    
    @singleton
    @provider
    def provideRoleApplicationService(self) -> RoleApplicationService:
        return RoleApplicationService(self.__injector__.get(RoleRepository))
    # endregion

    # region Repository
    @singleton
    @provider
    def provideUserRepository(self) -> UserRepository:
        return UserRepositoryImpl()
    
    @singleton
    @provider
    def provideRoleRepository(self) -> RoleRepository:
        return RoleRepositoryImpl()
    # endregion

    # region Messaging
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
    # endregion


class Builder:
    @classmethod
    def buildConsumer(cls, groupId: str = uuid4(), autoCommit: bool = False,
                      partitionEof: bool = True, autoOffsetReset: str = ConsumerOffsetReset.earliest.name) -> Consumer:
        builder = instance.get(ClassAssistedBuilder[KafkaConsumer])
        return builder.build(groupId=groupId, autoCommit=autoCommit, partitionEof=partitionEof,
                             autoOffsetReset=autoOffsetReset)


instance = Injector([AppDi])
