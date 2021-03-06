"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

import src.domain_model.ou.Ou as Ou
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__OuUpdated, "CommonEventConstant.OU_UPDATED.value", "message", "event")
"""


class OuUpdated(DomainEvent):
    def __init__(self, oldOu: Ou, newOu: Ou):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.OU_UPDATED.value)
        self._data = {"old": oldOu.toMap(), "new": newOu.toMap()}
