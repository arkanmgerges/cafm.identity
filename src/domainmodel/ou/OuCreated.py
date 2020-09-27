"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.ou.Ou import Ou


class OuCreated(DomainEvent):
    def __init__(self, ou: Ou):
        super().__init__()
        self._data = json.dumps(ou.toMap())

