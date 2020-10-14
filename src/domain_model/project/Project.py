"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Project:
    def __init__(self, id: str = None, name=''):
        self._id = str(uuid4()) if id is None else id
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        project = Project(id, name)
        if publishEvent:
            from src.domain_model.event.DomainEventPublisher import DomainEventPublisher
            from src.domain_model.project.ProjectCreated import ProjectCreated
            logger.debug(f'[{Project.createFrom.__qualname__}] - Create Project with name = {name} and id = {id}')
            DomainEventPublisher.addEventForPublishing(ProjectCreated(project))
        return project

    def id(self) -> str:
        return self._id

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if 'name' in data and data['name'] != self._name:
            updated = True
            self._name = data['name']
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.project.ProjectDeleted import ProjectDeleted
        DomainEventPublisher.addEventForPublishing(ProjectDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.project.ProjectUpdated import ProjectUpdated
        DomainEventPublisher.addEventForPublishing(ProjectUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __eq__(self, other):
        if not isinstance(other, Project):
            raise NotImplementedError(f'other: {other} is can not be compared with Project class')
        return self.id() == other.id() and self.name() == other.name()
