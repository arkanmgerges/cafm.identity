"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.exception.RealmAlreadyExistException import RealmAlreadyExistException
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.decorator import debugLogger


class RealmService:
    def __init__(self, realmRepo: RealmRepository, policyRepo: PolicyRepository):
        self._repo = realmRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createRealm(self, id: str = '', name: str = '', objectOnly: bool = False, tokenData: TokenData = None):
        try:
            if id == '':
                raise RealmDoesNotExistException()
            self._repo.realmByName(name=name)
            raise RealmAlreadyExistException(name)
        except RealmDoesNotExistException:
            if objectOnly:
                return Realm.createFrom(name=name)
            else:
                realm = Realm.createFrom(id=id, name=name, publishEvent=True)
                self._repo.createRealm(realm=realm, tokenData=tokenData)
                return realm

    @debugLogger
    def deleteRealm(self, realm: Realm, tokenData: TokenData = None):
        self._repo.deleteRealm(realm, tokenData=tokenData)
        realm.publishDelete()

    @debugLogger
    def updateRealm(self, oldObject: Realm, newObject: Realm, tokenData: TokenData = None):
        self._repo.updateRealm(newObject, tokenData=tokenData)
        newObject.publishUpdate(oldObject)
