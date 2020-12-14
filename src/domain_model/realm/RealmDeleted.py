"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.realm.Realm as Realm


class RealmDeleted(DomainEvent):
    def __init__(self, realm: Realm):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.REALM_DELETED.value)
        self._data = realm.toMap()
