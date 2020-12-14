"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.realm.Realm import Realm


class RealmUpdated(DomainEvent):
    def __init__(self, oldRealm: Realm, newRealm: Realm):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.REALM_UPDATED.value)
        self._data = {'old': oldRealm.toMap(), 'new': newRealm.toMap()}

