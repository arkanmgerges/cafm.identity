"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Realm:
    def __init__(self, id: str = str(uuid4()), name=''):
        self._id = id
        self._name = name

    @classmethod
    def createNew(cls, id: str = str(uuid4()), name=''):
        from src.domainmodel.event.DomainEventPublisher import DomainEventPublisher
        from src.domainmodel.realm.RealmCreated import RealmCreated

        realm = Realm(id, name)
        DomainEventPublisher.addEventForPublishing(RealmCreated(realm))
        return realm

    @classmethod
    def createFrom(cls, id: str = str(uuid4()), name=''):
        return Realm(id, name)

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}
