"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.realm.Realm import Realm


class RealmCreated(DomainEvent):
    def __init__(self, realm: Realm):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.REALM_CREATED.value)
        self._data = realm.toMap()

