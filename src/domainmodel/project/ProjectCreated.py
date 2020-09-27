"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

from src.domainmodel.event.DomainEvent import DomainEvent
from src.domainmodel.project.Project import Project


class ProjectCreated(DomainEvent):
    def __init__(self, project: Project):
        super().__init__()
        self._data = json.dumps(project.toMap())

