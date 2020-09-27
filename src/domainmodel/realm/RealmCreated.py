"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.realm.Realm import Realm


class RealmCreated(DomainEvent):
    def __init__(self, realm: Realm):
        super().__init__()
        self._data = json.dumps(realm.toMap())

