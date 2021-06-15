from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.resource.Resource import Resource


class ProjectToRealmAssigned(DomainEvent):
    def __init__(self, project: Resource, realm: Resource):
        super().__init__(
            id=str(uuid4()),
            name=CommonEventConstant.PROJECT_TO_REALM_ASSIGNED.value,
        )
        self._data = {"realm_id": realm.id(), "project_id": project.id()}
