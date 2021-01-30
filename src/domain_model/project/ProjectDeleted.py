"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.event.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
import src.domain_model.project.Project as Project

"""
c4model|cb|identity:ComponentQueue(identity__domainmodel_event__ProjectDeleted, "CommonEventConstant.PROJECT_DELETED.value", "message", "event")
"""
class ProjectDeleted(DomainEvent):
    def __init__(self, project: Project):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PROJECT_DELETED.value)
        self._data = project.toMap()
