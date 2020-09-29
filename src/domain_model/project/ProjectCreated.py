"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domain_model.event.DomainEvent import DomainEvent
from src.domain_model.project.Project import Project


class ProjectCreated(DomainEvent):
    def __init__(self, project: Project):
        super().__init__()
        self._data = json.dumps(project.toMap())

