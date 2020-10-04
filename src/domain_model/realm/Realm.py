"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Realm:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name='', publishEvent: bool = False):
        realm = Realm(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.realm.RealmCreated import RealmCreated
            logger.debug(f'[{Realm.createFrom.__qualname__}] - Create Realm with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(RealmCreated(realm))
        return realm

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
