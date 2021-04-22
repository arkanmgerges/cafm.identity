"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__UserToRealmAssigned, "CommonEventConstant.USER_TO_REALM_ASSIGNED.value", "message", "event")
"""


class UserToRealmAssigned(DomainEvent):
    def __init__(self, user: Resource, realm: Resource):
        super().__init__(
            id=str(uuid4()), name=CommonEventConstant.USER_TO_REALM_ASSIGNED.value
        )
        self._data = {"realm_id": realm.id(), "user_id": user.id()}
