"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
from uuid import uuid4

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.project.Project import Project


class ProjectCreated(DomainEvent):
    def __init__(self, project: Project):
        super().__init__(id=str(uuid4()), name=CommonEventConstant.PROJECT_CREATED.value)
        self._data = project.toMap()

