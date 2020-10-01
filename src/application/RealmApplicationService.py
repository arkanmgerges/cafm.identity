"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository


class RealmApplicationService:
    def __init__(self, realmRepository: RealmRepository):
        self._realmRepository = realmRepository

    def createObjectOnly(self, name: str):
        try:
            self._realmRepository.realmByName(name=name)
            raise RealmAlreadyExistException(name=name)
        except RealmDoesNotExistException:
            return Realm.createFrom(name=name)

    def createRealm(self, id: str, name: str):
        try:
            self._realmRepository.realmByName(name=name)
            raise RealmAlreadyExistException(name=name)
        except RealmDoesNotExistException:
            realm = Realm.createFrom(id=id, name=name, publishEvent=True)
            self._realmRepository.createRealm(realm)

    def realmByName(self, name: str):
        return self._realmRepository.realmByName(name=name)
