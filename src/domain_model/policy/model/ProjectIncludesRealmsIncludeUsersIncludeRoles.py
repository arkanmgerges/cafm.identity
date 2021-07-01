"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.common.HasToMap import HasToMap
from src.domain_model.policy.model.RealmIncludesUsersIncludeRoles import RealmIncludesUsersIncludeRoles
from src.domain_model.project.Project import Project


class ProjectIncludesRealmsIncludeUsersIncludeRoles(HasToMap):
    def __init__(self, project: Project, realmsIncludeUsersIncludeRoles: List[RealmIncludesUsersIncludeRoles]):
        self._project = project
        self._realmsIncludeUsersIncludeRoles = realmsIncludeUsersIncludeRoles if realmsIncludeUsersIncludeRoles is not None else []

    @classmethod
    def createFrom(cls, project: Project, realmsIncludeUsersIncludeRoles: List[RealmIncludesUsersIncludeRoles], **_kwargs):
        return ProjectIncludesRealmsIncludeUsersIncludeRoles(project=project, realmsIncludeUsersIncludeRoles=realmsIncludeUsersIncludeRoles)

    def id(self) -> str:
        return self._project.id()

    def name(self) -> str:
        return self._project.name()

    def realmsIncludeUsersIncludeRoles(self) -> List[RealmIncludesUsersIncludeRoles]:
        return self._realmsIncludeUsersIncludeRoles

    def toMap(self) -> dict:
        return {**self._project.toMap(), **{"realms_include_users_include_roles": [x.toMap() for x in self._realmsIncludeUsersIncludeRoles]}}

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

