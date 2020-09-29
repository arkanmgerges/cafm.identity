"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

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