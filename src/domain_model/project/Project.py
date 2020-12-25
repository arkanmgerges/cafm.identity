"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Project(Resource):
    def __init__(self, id: str = None, name=''):
        anId = str(uuid4()) if id is None or id == '' else id
        super().__init__(id=anId, type='project')
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name='', publishEvent: bool = False):
        project = Project(id, name)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
            from src.domain_model.project.ProjectCreated import ProjectCreated
            logger.debug(f'[{Project.createFrom.__qualname__}] - Create Project with name = {name} and id = {id}')
            DomainPublishedEvents.addEventForPublishing(ProjectCreated(project))
        return project

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
        DomainPublishedEvents.addEventForPublishing(ProjectDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.project.ProjectUpdated import ProjectUpdated
        DomainPublishedEvents.addEventForPublishing(ProjectUpdated(old, self))

    def toMap(self) -> dict:
        return {"id": self.id(), "name": self.name()}

    def __repr__(self):
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __str__(self) -> str:
        return f'<{self.__module__} object at {hex(id(self))}> {self.toMap()}'

    def __eq__(self, other):
        if not isinstance(other, Project):
            raise NotImplementedError(f'other: {other} can not be compared with Project class')
        return self.id() == other.id() and self.name() == other.name()
