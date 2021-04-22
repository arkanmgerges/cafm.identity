"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.ou.Ou as Ou

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__OuDeleted, "CommonEventConstant.OU_DELETED.value", "message", "event")
"""


class OuDeleted(DomainEvent):
    def __init__(self, ou: Ou):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.OU_DELETED.value)
        self._data = ou.toMap()
