"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List, Any

from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.common.Resource import Resource
from src.domain_model.permission.Permission import Permission
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException import \
    ResourceAssignmentAlreadyExistException
from src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException import \
    ResourceAssignmentDoesNotExistException
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType
from src.domain_model.role.Role import Role
from src.domain_model.user.User import User
from src.domain_model.user_group.UserGroup import UserGroup
from src.resource.logging.logger import logger


class PolicyRepositoryImpl(PolicyRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
        except Exception as e:
            logger.warn(f'[{PolicyRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def allTreeByRoleName(self, roleName: str) -> List[Any]:
        # aql = '''
        #     FOR u IN project
        #     FILTER u.id == @id
        #     RETURN u
        # '''
        #
        # bindVars = {"id": id}
        # queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        # result = queryResult.result
        # if len(result) == 0:
        #     raise ProjectDoesNotExistException(name=f'project id: {id}')
        #
        # return Project.createFrom(id=result[0]['id'], name=result[0]['name'])
        return []

    def roleDocumentId(self, role):
        # Get the role doc id
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'role'
                RETURN d
        '''
        bindVars = {"id": role.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PolicyRepositoryImpl.roleDocumentId.__qualname__}] role id: {role.id()}')
            raise RoleDoesNotExistException(
                f'role id: {role.id()}')
        result = result[0]
        roleDocId = result['_id']
        return roleDocId

    def userDocumentId(self, user):
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                RETURN d
        '''
        bindVars = {"id": user.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PolicyRepositoryImpl.userDocumentId.__qualname__}] user id: {user.id()}')
            raise UserDoesNotExistException(
                f'user id: {user.id()}')
        result = result[0]
        userDocId = result['_id']
        return userDocId

    def userGroupDocumentId(self, userGroup):
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user_group'
                RETURN d
        '''
        bindVars = {"id": userGroup.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PolicyRepositoryImpl.userGroupDocumentId.__qualname__}] user group id: {userGroup.id()}')
            raise UserGroupDoesNotExistException(
                f'user group id: {userGroup.id()}')
        result = result[0]
        userDocId = result['_id']
        return userDocId

    # region Assignment Role - User
    def assignRoleToUser(self, role: Role, user: User) -> None:
        userDocId = self.userDocumentId(user)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.assignmentRoleToUser(roleDocId, userDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignRoleToUser.__qualname__}] Resource already assigned for user: {user.id()}, role: {role.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned for user: {user.id()}, role: {role.id()}')

        # Assign a role to the user
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'user', to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'user', to_type: 'role'}
                  IN has                  
                '''
        bindVars = {"fromId": userDocId, "toId": roleDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeRoleFromUser(self, role: Role, user: User) -> None:
        userDocId = self.userDocumentId(user)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUser(roleDocId, userDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Resource assignment for user: {user.id()} and role: {role.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for user: {user.id()} and role: {role.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        bindVars = {"_id": result['_id']}
        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Revoke role with id: {role.id()} from user with id: {user.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    def assignmentRoleToUser(self, roleDocId, userDocId) -> List:
        # Check if there is a link
        aql = '''
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d.from_type == 'user' AND d.to_type == 'role'
              RETURN d
        '''
        bindVars = {"fromId": userDocId, "toId": roleDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment Role - User Group
    def assignRoleToUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.assignmentRoleToUserGroup(roleDocId, userGroupDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignRoleToUserGroup.__qualname__}] Resource already assigned for user group: {userGroup.id()}, role: {role.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned for user group: {userGroup.id()}, role: {role.id()}')

        # Assign a role to the user group
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'user_group', to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'user_group', to_type: 'role'}
                  IN has                  
                '''
        bindVars = {"fromId": userGroupDocId, "toId": roleDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeRoleFromUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUserGroup(roleDocId, userGroupDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Resource assignment for user group: {userGroup.id()} and role: {role.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for user group: {userGroup.id()} and role: {role.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        bindVars = {"_id": result['_id']}
        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke role with id: {role.id()} from user group with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    def assignmentRoleToUserGroup(self, roleDocId, userGroupDocId) -> List:
        # Check if there is a link
        aql = '''
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d.from_type == 'user_group' AND d.to_type == 'role'
              RETURN d
        '''
        bindVars = {"fromId": userGroupDocId, "toId": roleDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment User - User Group
    def assignUserToUserGroup(self, user: User, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        userDocId = self.userDocumentId(user)

        # Check if there is any already exist link?
        result = self.assignmentUserToUserGroup(userDocId, userGroupDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignUserToUserGroup.__qualname__}] Resource already assigned for user group: {userGroup.id()}, user: {user.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned for user group: {userGroup.id()}, user: {user.id()}')

        # Assign a user to the user group
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'user_group', to_type: 'user'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'user_group', to_type: 'user'}
                  IN has                  
                '''
        bindVars = {"fromId": userGroupDocId, "toId": userDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeUserFromUserGroup(self, user: User, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        userDocId = self.userDocumentId(user)
        result = self.assignmentUserToUserGroup(userDocId, userGroupDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Resource assignment for user group: {userGroup.id()} and user: {user.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for user group: {userGroup.id()} and user: {user.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        bindVars = {"_id": result['_id']}
        logger.debug(
            f'[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Revoke user with id: {user.id()} from user group with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    def assignmentUserToUserGroup(self, userDocId, userGroupDocId) -> List:
        # Check if there is a link
        aql = '''
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d.from_type == 'user_group' AND d.to_type == 'user'
              RETURN d
        '''
        bindVars = {"fromId": userGroupDocId, "toId": userDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment Role - Permission - Resource type
    def assignRoleToPermissionForResourceType(self, role: Role, permission: Permission,
                                              resourceType: ResourceType) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)
        resourceTypeDocId = self.resourceTypeDocumentId(resourceType)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermissionForResourceType(roleDocId, permissionDocId, resourceTypeDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignRoleToPermissionForResourceType.__qualname__}] Resource already assigned role id: {role.id()}, permission: {permission.id()}, resource type id: {resourceType.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned role id: {role.id()}, permission: {permission.id()}, resource type id: {resourceType.id()}')

        # Assign the role to the permission
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'role', to_type: 'permission'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'role', to_type: 'permission'}
                  IN `has`                  
                '''
        bindVars = {"fromId": roleDocId, "toId": permissionDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        # Assign the permission to resource type
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'permission', to_type: 'resource_type'}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'permission', to_type: 'resource_type'}
                  IN `for`                  
                '''
        bindVars = {"fromId": permissionDocId, "toId": resourceTypeDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def permissionDocumentId(self, permission: Permission):
        # Get the doc id
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'permission'
                RETURN d
        '''
        bindVars = {"id": permission.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PolicyRepositoryImpl.permissionDocumentId.__qualname__}] permission id: {permission.id()}')
            raise PermissionDoesNotExistException(
                f'permission id: {permission.id()}')
        result = result[0]
        docId = result['_id']
        return docId

    def resourceTypeDocumentId(self, resourceType: ResourceType):
        # Get the doc id
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'resource_type'
                RETURN d
        '''
        bindVars = {"id": resourceType.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.resourceTypeDocumentId.__qualname__}] resource type id: {resourceType.id()}')
            raise ResourceTypeDoesNotExistException(
                f'resource type id: {resourceType.id()}')
        result = result[0]
        docId = result['_id']
        return docId

    def assignmentRoleToPermissionForResourceType(self, roleDocId, permissionDocId, resourceTypeDocId) -> List:
        # Check if there is a link
        aql = '''
            WITH `has`, `for`, `resource`
            FOR d IN `resource`
                FILTER d._id == @roleDocId AND d.type == 'role'
                LET r = (
                    FOR v1,e1 IN OUTBOUND d._id `has` FILTER e1.to_type == "permission" AND v1._id == @permissionDocId
                        FOR v2,e2 IN OUTBOUND v1._id `for` FILTER e2.to_type == "resource_type" AND v2._id == @resourceTypeDocId
                            RETURN  {"permission": v1, "resource_type": v2, "to_permission_edge": e1, "to_resource_type_edge": e2}
                )
                FILTER LENGTH(r) > 0
                RETURN {"role": d, "permission_with_resource_type": r}
        '''
        bindVars = {"roleDocId": roleDocId, "permissionDocId": permissionDocId, "resourceTypeDocId": resourceTypeDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    def revokeRoleFromPermissionForResourceType(self, role: Role, permission: Permission,
                                                resourceType: ResourceType) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)
        resourceTypeDocId = self.resourceTypeDocumentId(resourceType)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermissionForResourceType(roleDocId, permissionDocId, resourceTypeDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeRoleFromPermissionForResourceType.__qualname__}] Resource assignment for role id: {role.id()}, permission id: {permission.id()}, resource type id: {resourceType.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for role id: {role.id()}, permission id: {permission.id()}, resource type id: {resourceType.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        for d in result['permission_with_resource_type']:
            bindVars = {"_id": d['to_permission_edge']['_id']}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

        aql = '''
            FOR d IN `for`
                FILTER d._id == @_id
                REMOVE d IN `for`
        '''
        for d in result['permission_with_resource_type']:
            bindVars = {"_id": d['to_resource_type_edge']['_id']}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke role with id: {role.id()} from permission with id: {permission.id()} for resource type with id: {resourceType.id()}')

    # endregion

    # region Access Role - Resource
    def provideAccessRoleToResource(self, role: Role, resource: Resource) -> None:
        resourceDocId = self.resourceDocumentId(resource)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.accessRoleToResource(roleDocId, resourceDocId, resource)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.provideAccessRoleToResource.__qualname__}] Resource already assigned for role: {role.id()}, resource: {resource.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned for role: {role.id()}, resource: {resource.id()}')

        # Assign a role to the user
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, from_type: 'role', to_type: @resourceTypeName}
                    UPDATE {_from: @fromId, _to: @toId, from_type: 'role', to_type: @resourceTypeName}
                  IN access                  
                '''
        bindVars = {"fromId": roleDocId, "toId": resourceDocId, "resourceTypeName": resource.type()}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeAccessRoleFromResource(self, role: Role, resource: Resource) -> None:
        resourceDocId = self.resourceDocumentId(resource)
        roleDocId = self.roleDocumentId(role)
        result = self.accessRoleToResource(roleDocId, resourceDocId, resource)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeAccessRoleFromResource.__qualname__}] Resource assignment for role: {role.id()} and resource: {resource.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for role: {role.id()} and resource: {resource.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN `access`
                FILTER d._id == @_id
                REMOVE d IN `access`
        '''
        bindVars = {"_id": result['_id']}
        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Revoke role with id: {role.id()} from resource with id: {resource.id()}, type: {resource.type()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    def accessRoleToResource(self, roleDocId, resourceDocId, resource: Resource) -> List:
        # Check if there is a link
        aql = '''
            FOR d IN access
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d.from_type == 'role' AND d.to_type == @resourceTypeName
              RETURN d
        '''
        bindVars = {"fromId": roleDocId, "toId": resourceDocId, "resourceTypeName": resource.type()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    def resourceDocumentId(self, resource: Resource):
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == @type
                RETURN d
        '''
        bindVars = {"id": resource.id(), "type": resource.type()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{PolicyRepositoryImpl.resourceDocumentId.__qualname__}] resource id: {resource.id()}')
            raise RoleDoesNotExistException(
                f'resource id: {resource.id()}')
        result = result[0]
        docId = result['_id']
        return docId

    # endregion
