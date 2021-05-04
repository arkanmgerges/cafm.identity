"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.project.Project import Project
from src.domain_model.token.TokenData import TokenData


class ProjectRepository(ABC):
    @abstractmethod
    def save(self, obj: Project, tokenData: TokenData):
        """Save project

        Args:
            obj (Project): The project that needs to be saved
            tokenData (TokenData): Token data that has info about the token

        """

    @abstractmethod
    def deleteProject(self, obj: Project, tokenData: TokenData) -> None:
        """Delete a project

        Args:
            obj (Project): The project that needs to be deleted
            tokenData (TokenData): Token data used for deleting the resource

        :raises:
            `ObjectCouldNotBeDeletedException <src.domain_model.resource.exception.ObjectCouldNotBeDeletedException>` Raise an exception if the project could not be deleted
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
    def projects(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        """Get list of projects based on the owned roles that the user has

        Args:
            tokenData (TokenData): A token data object
            roleAccessPermissionData (List[RoleAccessPermissionData]): List of role access permissions
            resultFrom (int): The start offset of the result item
            resultSize (int): The size of the items in the result
            order (List[dict]): A list of order e.g. [{'orderBy': 'name', 'direction': 'asc'}, {'orderBy': 'age', 'direction': 'desc'}]

        Returns:
            dict: A dict that has {"items": [], "totalItemCount": 0}
        """
