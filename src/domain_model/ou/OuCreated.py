"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.ou.Ou import Ou


class OuCreated(DomainEvent):
    def __init__(self, ou: Ou):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.OU_CREATED.value)
        self._data = ou.toMap()

