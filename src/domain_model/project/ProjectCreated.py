"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.project.Project import Project

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__ProjectCreated, "Project Created", "event", "message")
"""
class ProjectCreated(DomainEvent):
    def __init__(self, project: Project):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PROJECT_CREATED.value)
        self._data = project.toMap()

