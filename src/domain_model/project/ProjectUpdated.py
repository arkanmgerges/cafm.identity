"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.EventConstant import CommonEventConstant
from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.project.Project import Project


class ProjectUpdated(DomainEvent):
    def __init__(self, oldProject: Project, newProject: Project):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PROJECT_UPDATED.value)
        self._data = {'old': oldProject.toMap(), 'new': newProject.toMap()}

