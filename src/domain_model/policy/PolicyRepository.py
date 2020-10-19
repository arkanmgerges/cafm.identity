"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List, Any

from src.domain_model.role.Role import Role
from src.domain_model.user.User import User
from src.domain_model.user_group.UserGroup import UserGroup


class PolicyRepository(ABC):
    @abstractmethod
    def allTreeByRoleName(self, roleName: str) -> List[Any]:
        """Retrieve all the connection by role name

        Args:
            roleName (str): Role name that is used to retrieve the connected nodes to it

        """

    @abstractmethod
    def assignRoleToUser(self, role: Role, user: User) -> None:
        """Assign role to user

        Args:
            role (Role): Role object to be assigned to user
            user (User): User object to have the role assigned to

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeRoleFromUser(self, role: Role, user: User) -> None:
        """Revoke role from user

        Args:
            role (Role): Role object to be revoked from user
            user (User): User object to remove the role that it has

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def assignRoleToUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        """Assign role to user group

        Args:
            role (Role): Role object to be assigned to user group
            userGroup (UserGroup): User group object to have the role assigned to

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeRoleFromUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        """Revoke role from user group

        Args:
            role (Role): Role object to be revoked from user group
            userGroup (UserGroup): User group object to remove the role that it has

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """