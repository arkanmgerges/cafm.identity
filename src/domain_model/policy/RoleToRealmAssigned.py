"""
@author: Mohammad S. moso<moso@develoop.run>
"""
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource
from src.domain_model.role.Role import Role

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__RoleToRealmAssigned, "CommonEventConstant.ROLE_TO_REALM_ASSIGNED.value", "message", "event")
"""


class RoleToRealmAssigned(DomainEvent):
    def __init__(self, role: Role, realm: Resource):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.ROLE_TO_REALM_ASSIGNED.value)
        self._data = {'role_id': role.id(), 'realm_id': realm.id()}
