"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.ou.Ou import Ou


class OuCreated(DomainEvent):
    def __init__(self, ou: Ou):
        super().__init__()
        self._data = json.dumps(ou.toMap())

