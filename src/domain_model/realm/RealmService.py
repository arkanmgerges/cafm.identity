"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.exception.RealmAlreadyExistException import (
    RealmAlreadyExistException,
)
from src.domain_model.resource.exception.RealmDoesNotExistException import (
    RealmDoesNotExistException,
)
from src.domain_model.token.TokenData import TokenData
from src.resource.logging.decorator import debugLogger


class RealmService:
    def __init__(self, realmRepo: RealmRepository, policyRepo: PolicyRepository):
        self._repo = realmRepo
        self._policyRepo = policyRepo

    @debugLogger
    def createRealm(
        self, obj: Realm, objectOnly: bool = False, tokenData: TokenData = None
    ):
        if objectOnly:
            return (
                Realm.createFromObject(obj=obj, generateNewId=True)
                if obj.id() == ""
                else obj
            )
        else:
            obj = Realm.createFromObject(obj=obj, publishEvent=True)
            self._repo.save(obj=obj, tokenData=tokenData)
            return obj

    @debugLogger
    def deleteRealm(self, obj: Realm, tokenData: TokenData = None):
        obj.publishDelete()
        self._repo.deleteRealm(obj, tokenData=tokenData)

    @debugLogger
    def updateRealm(
        self, oldObject: Realm, newObject: Realm, tokenData: TokenData = None
    ):
        newObject.publishUpdate(oldObject)
        self._repo.save(obj=newObject, tokenData=tokenData)
