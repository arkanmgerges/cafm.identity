"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from copy import copy

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.resource.Resource import Resource
from src.domain_model.event.DomainPublishedEvents import DomainPublishedEvents
from src.resource.logging.logger import logger

"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4


class Project(Resource, HasToMap):
    def __init__(self, id: str = None, name="", skipValidation: bool = False):
        anId = str(uuid4()) if id is None else id
        super().__init__(id=anId, type="project")
        self._name = name

    @classmethod
    def createFrom(cls, id: str = None, name="", publishEvent: bool = False, skipValidation: bool = False, **_kwargs):
        project = Project(id, name, skipValidation=skipValidation)
        if publishEvent:
            from src.domain_model.event.DomainPublishedEvents import (
                DomainPublishedEvents,
            )
            from src.domain_model.project.ProjectCreated import ProjectCreated

            logger.debug(
                f"[{Project.createFrom.__qualname__}] - Create Project with name = {name} and id = {id}"
            )
            DomainPublishedEvents.addEventForPublishing(ProjectCreated(project))
        return project

    @classmethod
    def createFromObject(
        cls, obj: "Project", publishEvent: bool = False, generateNewId: bool = False
    ):
        logger.debug(f"[{Project.createFromObject.__qualname__}]")
        id = None if generateNewId else obj.id()
        return cls.createFrom(id=id, name=obj.name(), publishEvent=publishEvent)

    def name(self) -> str:
        return self._name

    def update(self, data: dict):
        updated = False
        old = copy(self)
        if "name" in data and data["name"] != self._name:
            updated = True
            self._name = data["name"]
        if updated:
            self.publishUpdate(old)

    def publishDelete(self):
        from src.domain_model.project.ProjectDeleted import ProjectDeleted

        DomainPublishedEvents.addEventForPublishing(ProjectDeleted(self))

    def publishUpdate(self, old):
        from src.domain_model.project.ProjectUpdated import ProjectUpdated

        DomainPublishedEvents.addEventForPublishing(ProjectUpdated(old, self))

    def toMap(self) -> dict:
        return {"project_id": self.id(), "name": self.name()}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __eq__(self, other):
        if not isinstance(other, Project):
            raise NotImplementedError(
                f"other: {other} can not be compared with Project class"
            )
        return self.id() == other.id() and self.name() == other.name()
