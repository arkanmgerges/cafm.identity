"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod
from typing import List, Any

from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.token.TokenData import TokenData
from src.domain_model.permission.Permission import Permission
from src.domain_model.resource.Resource import Resource
from src.domain_model.permission_context.PermissionContext import PermissionContext
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

    @abstractmethod
    def assignUserToUserGroup(self, user: User, userGroup: UserGroup) -> None:
        """Assign user to user group

        Args:
            user (User): User object to be assigned to user group
            userGroup (UserGroup): User group object to have the user assigned to

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeUserFromUserGroup(self, user: User, userGroup: UserGroup) -> None:
        """Revoke user from user group

        Args:
            user (User): User object to be revoked from user group
            userGroup (UserGroup): User group object to remove the user that it has

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def assignRoleToPermission(self, role: Role, permission: Permission) -> None:
        """Assign a role to a permission

        Args:
            role (Role): The role to be assigned to the permission
            permission (Permission): The permission that will get a role

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeAssignmentRoleToPermission(self, role: Role, permission: Permission) -> None:
        """Revoke a role from a permission

        Args:
            role (Role): The role to be revoked from the permission
            permission (Permission): The permission that will be separated from the role

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def assignPermissionToPermissionContext(self, permission: Permission, permissionContext: PermissionContext) -> None:
        """Assign permission to a permission context

        Args:
            permission (Permission): The permission to be assigned to a permission context
            permissionContext (PermissionContext): The permission context to be linked to the permission

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeAssignmentPermissionToPermissionContext(self, permission: Permission, permissionContext: PermissionContext) -> None:
        """Revoke assignment of a permission to a permission context

        Args:
            permission (Permission): The permission that will be separated from the permission context
            permissionContext (PermissionContext): The permission context to be unlinked from the permission

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def provideAccessRoleToResource(self, role: Role, resource: Resource) -> None:
        """Make a link access for a role to a resource

        Args:
            role (Role): The role to have access to the resource
            resource (Resource): The resource that the role has access to

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeAccessRoleFromResource(self, role: Role, resource: Resource) -> None:
        """Revoke the link access of a role to a resource

        Args:
            role (Role): The role to unlink the access to the resource
            resource (Resource): The resource that the role will be unlinked from it

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def assignResourceToResource(self, resourceSrc: Resource, resourceDst: Resource) -> None:
        """Make an assignment from a resource to another resource

        Args:
            resourceSrc (Resource): The source resource to assign to
            resourceDst (Resource): The destination resource that will be attached to

        :raises:
            `ResourceAssignmentAlreadyExistException <src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException>` Raise an exception if the resource assignment already exist
        """

    @abstractmethod
    def revokeAssignmentResourceToResource(self, resourceSrc: Resource, resourceDst: Resource) -> None:
        """Revoke assignment from a resource to another resource

        Args:
            resourceSrc (Resource): The source resource to revoke the assignment from
            resourceDst (Resource): The destination resource that will be detached to

        :raises:
            `ResourceAssignmentDoesNotExistException <src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException>` Raise an exception if the resource assignment does not exist
        """

    @abstractmethod
    def connectResourceToOwner(self, resource: Resource, tokenData: TokenData) -> None:
        """Link a resource to the owner

        Args:
            resource (Resource): A resource that is to be connected to the owner
            tokenData (TokenData): Token info that is used to connect extract the owner
        """

    @abstractmethod
    def roleAccessPermissionsData(self, tokenData: TokenData, includeAccessTree: bool) -> List[RoleAccessPermissionData]:
        """Retrieve the permissions and permission contexts connected to it also related to the roles that belong
        to the token provided

        Args:
            tokenData (TokenData): A token info
            includeAccessTree (bool): Include the access tree if this is set to True, otherwise don't include it

        Returns:
            List[RoleAccessPermissionData]: A list of role with access and permissions with permission contexts
        """

    @abstractmethod
    def isOwnerOfResource(self, resource: Resource, tokenData: TokenData) -> bool:
        """Check of the resource is owned by the user/role in the token data

        Args:
            resource (Resource): The resource to be checked for ownership
            tokenData (TokenData): Token info that is used to check for the ownership of the resource

        Returns:
            bool: Returns True if the user/role in the token data is the owner of the resource, False otherwise
        """

    @abstractmethod
    def resourcesOfTypeByTokenData(self, resourceType: str = '', tokenData: TokenData = None,
                                   roleAccessPermissionData: List[RoleAccessPermissionData] = None, sortData: str = '') -> dict:
        """Get resources that is filtered by the allowed permissions

        Args:
            resourceType (str): A resource type string (ex. realm, ou, project ...etc)
            tokenData (TokenData): Token data that has information about the user/role
            roleAccessPermissionData (RoleAccessPermissionData): Role with permission data and access tree
            sortData (str): A string for sorting the data

        Returns:
            dict: A dictionary that has 'items' as an array
        """