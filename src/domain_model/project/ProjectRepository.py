"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.project.Project import Project


class ProjectRepository(ABC):
    @abstractmethod
    def createProject(self, project: Project):
        """Create project

        Args:
            project (Project): The project that needs to be created

        """

    @abstractmethod
    def projectByName(self, name: str) -> Project:
        """Get project by name

        Args:
            name (str): The name of the project

        Returns:
            Project: project object
        """

    @abstractmethod
    def projectById(self, id: str) -> Project:
        """Get project by id

        Args:
            id (str): The id of the project

        Returns:
            Project: project object
        """

    @abstractmethod
    def projectsByOwnedProjects(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100) -> List[Project]:
        """Get list of projects based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result

        Returns:
            List[Project]: A list of projects
        """