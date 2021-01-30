"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.realm.Realm import Realm

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RealmCreated, "CommonEventConstant.REALM_CREATED.value", "message", "event")
"""
class RealmCreated(DomainEvent):
    def __init__(self, realm: Realm):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.REALM_CREATED.value)
        self._data = realm.toMap()

