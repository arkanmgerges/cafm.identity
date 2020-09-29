from uuid import uuid4

from injector import Module, Injector, singleton, provider, inject

from src.application.OuApplicationService import OuApplicationService
from src.application.PermissionApplicationService import PermissionApplicationService
from src.application.ProjectApplicationService import ProjectApplicationService
from src.application.RealmApplicationService import RealmApplicationService
from src.application.ResourceTypeApplicationService import ResourceTypeApplicationService
from src.application.RoleApplicationService import RoleApplicationService
from src.application.UserApplicationService import UserApplicationService
from src.application.UserGroupApplicationService import UserGroupApplicationService
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.permission.PermissionRepository import PermissionRepository
from src.domain_model.project.ProjectRepository import ProjectRepository
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource_type.ResourceTypeRepository import ResourceTypeRepository
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.user.UserRepository import UserRepository
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.port_adapter.messaging.common.Consumer import Consumer
from src.port_adapter.messaging.common.ConsumerOffsetReset import ConsumerOffsetReset
from src.port_adapter.messaging.common.SimpleProducer import SimpleProducer
from src.port_adapter.messaging.common.TransactionalProducer import TransactionalProducer
from src.port_adapter.messaging.common.kafka.KafkaConsumer import KafkaConsumer
from src.port_adapter.messaging.common.kafka.KafkaProducer import KafkaProducer
from injector import ClassAssistedBuilder

from src.port_adapter.repository.arangodb.ou.OuRepositoryImpl import OuRepositoryImpl
from src.port_adapter.repository.arangodb.permission.PermissionRepositoryImpl import PermissionRepositoryImpl
from src.port_adapter.repository.arangodb.project.ProjectRepositoryImpl import ProjectRepositoryImpl
from src.port_adapter.repository.arangodb.realm.RealmRepositoryImpl import RealmRepositoryImpl
from src.port_adapter.repository.arangodb.resource_type.ResourceTypeRepositoryImpl import ResourceTypeRepositoryImpl
from src.port_adapter.repository.arangodb.role.RoleRepositoryImpl import RoleRepositoryImpl
from src.port_adapter.repository.arangodb.user.UserRepositoryImpl import UserRepositoryImpl
from src.port_adapter.repository.arangodb.user_group.UserGroupRepositoryImpl import UserGroupRepositoryImpl


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
    
    @singleton
    @provider
    def provideOuApplicationService(self) -> OuApplicationService:
        return OuApplicationService(self.__injector__.get(OuRepository))
    
    @singleton
    @provider
    def provideRealmApplicationService(self) -> RealmApplicationService:
        return RealmApplicationService(self.__injector__.get(RealmRepository))

    @singleton
    @provider
    def providePermissionApplicationService(self) -> PermissionApplicationService:
        return PermissionApplicationService(self.__injector__.get(PermissionRepository))
    
    @singleton
    @provider
    def provideProjectApplicationService(self) -> ProjectApplicationService:
        return ProjectApplicationService(self.__injector__.get(ProjectRepository))
    
    @singleton
    @provider
    def provideResourceTypeApplicationService(self) -> ResourceTypeApplicationService:
        return ResourceTypeApplicationService(self.__injector__.get(ResourceTypeRepository))

    @singleton
    @provider
    def provideUserGroupApplicationService(self) -> UserGroupApplicationService:
        return UserGroupApplicationService(self.__injector__.get(UserGroupRepository))
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
    
    @singleton
    @provider
    def provideOuRepository(self) -> OuRepository:
        return OuRepositoryImpl()
    
    @singleton
    @provider
    def provideRealmRepository(self) -> RealmRepository:
        return RealmRepositoryImpl()
    
    @singleton
    @provider
    def providePermissionRepository(self) -> PermissionRepository:
        return PermissionRepositoryImpl()
    
    @singleton
    @provider
    def provideProjectRepository(self) -> ProjectRepository:
        return ProjectRepositoryImpl()
    
    @singleton
    @provider
    def provideResourceTypeRepository(self) -> ResourceTypeRepository:
        return ResourceTypeRepositoryImpl()

    @singleton
    @provider
    def provideUserGroupRepository(self) -> UserGroupRepository:
        return UserGroupRepositoryImpl()
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
