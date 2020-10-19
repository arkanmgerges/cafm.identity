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

        :raises:
            `ProjectDoesNotExistException <src.domain_model.resource.exception.ProjectDoesNotExistException>` Raise an exception if the project does not exist            
        """

    @abstractmethod
    def projectById(self, id: str) -> Project:
        """Get project by id

        Args:
            id (str): The id of the project

        Returns:
            Project: project object

        :raises:
            `ProjectDoesNotExistException <src.domain_model.resource.exception.ProjectDoesNotExistException>` Raise an exception if the project does not exist            
        """

    @abstractmethod
    def projectsByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                             order: List[dict] = None) -> dict:
        """Get list of projects based on the owned roles that the user has

        Args:
            ownedRoles (List[str]): A list of the roles that the user or user group has
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "itemCount": 0}
        """

    @abstractmethod
    def deleteProject(self, project: Project) -> None:
        """Delete a project

        Args:
            project (Project): The project that needs to be deleted
            
        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the project could not be deleted            
        """

    @abstractmethod
    def updateProject(self, project: Project) -> None:
        """Update a project

        Args:
            project (Project): The project that needs to be updated
            
        :raises:
            `ObjectCouldNotBeUpdatedException <src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException>` Raise an exception if the project could not be updated
        """
