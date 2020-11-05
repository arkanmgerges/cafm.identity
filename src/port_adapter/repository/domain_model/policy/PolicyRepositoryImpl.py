"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from collections import defaultdict
from typing import List, Any, Dict

from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.permission.Permission import Permission
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithResourceTypes import PermissionWithResourceTypes
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.PermissionDoesNotExistException import PermissionDoesNotExistException
from src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException import \
    ResourceAssignmentAlreadyExistException
from src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException import \
    ResourceAssignmentDoesNotExistException
from src.domain_model.resource.exception.ResourceTypeDoesNotExistException import ResourceTypeDoesNotExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.resource_type.ResourceType import ResourceType, ResourceTypeConstant
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenData import TokenData
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

    def roleDocumentId(self, role: Role):
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

    def userDocumentId(self, user: User):
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

    def userGroupDocumentId(self, userGroup: UserGroup):
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
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user', _to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user', _to_type: 'role'}
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
                AND d._from_type == 'user' AND d._to_type == 'role'
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
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'role'}
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
                AND d._from_type == 'user_group' AND d._to_type == 'role'
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
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'user'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'user'}
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
                AND d._from_type == 'user_group' AND d._to_type == 'user'
              RETURN d
        '''
        bindVars = {"fromId": userGroupDocId, "toId": userDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment Role - Permission - Resource type
    def assignRoleToPermission(self, role: Role, permission: Permission) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermission(roleDocId, permissionDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignRoleToPermission.__qualname__}] Resource already assigned role id: {role.id()}, permission: {permission.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned role id: {role.id()}, permission: {permission.id()}')

        # Assign the role to the permission
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: 'permission'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: 'permission'}
                  IN `has`                  
                '''
        bindVars = {"fromId": roleDocId, "toId": permissionDocId}
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

    def assignmentRoleToPermission(self, roleDocId, permissionDocId) -> List:
        # Check if there is a link
        aql = '''
            WITH `has`, `for`, `resource`
            FOR d IN `resource`
                FILTER d._id == @roleDocId AND d.type == 'role'
                LET r = (
                    FOR v1,e1 IN OUTBOUND d._id `has` FILTER e1._to_type == "permission" AND v1._id == @permissionDocId
                        RETURN  {"permission": v1, "to_permission_edge": e1}
                )
                FILTER LENGTH(r) > 0
                RETURN {"role": d, "permission": r}
        '''
        bindVars = {"roleDocId": roleDocId, "permissionDocId": permissionDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    def revokeAssignmentRoleToPermission(self, role: Role, permission: Permission) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermission(roleDocId, permissionDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeAssignmentRoleToPermission.__qualname__}] Resource not exist for assignment a role id: {role.id()} to permission id: {permission.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for role id: {role.id()}, permission id: {permission.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        for d in result['permission']:
            bindVars = {"_id": d['to_permission_edge']['_id']}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke assignment of role with id: {role.id()} to permission with id: {permission.id()}')

    def assignPermissionToResourceType(self, permission: Permission, resourceType: ResourceType) -> None:
        permissionDocId = self.permissionDocumentId(permission)
        resourceTypeDocId = self.resourceTypeDocumentId(resourceType)

        # Check if there is any already exist link?
        result = self.assignmentPermissionToResourceType(permissionDocId, resourceTypeDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignPermissionToResourceType.__qualname__}] Resource already assigned permission: {permission.id()}, resource type id: {resourceType.id()}')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned permission: {permission.id()}, resource type id: {resourceType.id()}')

        # Assign the permission to resource type
        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'resource_type'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'resource_type'}
                  IN `for`                  
                '''
        bindVars = {"fromId": permissionDocId, "toId": resourceTypeDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def assignmentPermissionToResourceType(self, permissionDocId, resourceTypeDocId) -> List:
        # Check if there is a link
        aql = '''
            WITH `for`, `resource`
            FOR d IN `resource`
                FILTER d._id == @permissionDocId AND d.type == 'permission'
                LET r = (
                    FOR v1,e1 IN OUTBOUND d._id `for` FILTER e1._to_type == "resource_type" AND v1._id == @resourceTypeDocId
                        RETURN  {"resource_type": v1, "to_resource_type_edge": e1}
                )
                FILTER LENGTH(r) > 0
                RETURN {"permission": d, "resource_type": r}
        '''
        bindVars = {"permissionDocId": permissionDocId, "resourceTypeDocId": resourceTypeDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    def revokeAssignmentPermissionToResourceType(self, permission: Permission, resourceType: ResourceType) -> None:
        permissionDocId = self.permissionDocumentId(permission)
        resourceTypeDocId = self.resourceTypeDocumentId(resourceType)

        # Check if there is any already exist link?
        result = self.assignmentPermissionToResourceType(permissionDocId, resourceTypeDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeAssignmentPermissionToResourceType.__qualname__}] Resource assignment for permission id: {permission.id()}, resource type id: {resourceType.id()}')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment for permission id: {permission.id()}, resource type id: {resourceType.id()}')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN `for`
                FILTER d._id == @_id
                REMOVE d IN `for`
        '''
        for d in result['resource_type']:
            bindVars = {"_id": d['to_resource_type_edge']['_id']}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

        logger.debug(
            f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke assignment permission with id: {permission.id()} to resource type with id: {resourceType.id()}')

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
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: @resourceTypeName}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: @resourceTypeName}
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
                AND d._from_type == 'role' AND d._to_type == @resourceTypeName
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

    # region Assignment Resource - Resource
    def assignResourceToResource(self, resourceSrc: Resource, resourceDst: Resource) -> None:
        resourceSrcDocId = self.resourceDocumentId(resourceSrc)
        resourceDstDocId = self.resourceDocumentId(resourceDst)

        # Check if there is any already exist link?
        result = self.assignmentResourceToResource(resourceSrcDocId, resourceDstDocId)
        if len(result) > 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.assignResourceToResource.__qualname__}] Resource already assigned, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})')
            raise ResourceAssignmentAlreadyExistException(
                f'Resource already assigned, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})')

        aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                  IN has                  
                '''
        bindVars = {"fromId": resourceSrcDocId, "toId": resourceDstDocId, "fromType": resourceSrc.type(),
                    "toType": resourceDst.type()}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeAssignmentResourceToResource(self, resourceSrc: Resource, resourceDst: Resource) -> None:
        resourceSrcDocId = self.resourceDocumentId(resourceSrc)
        resourceDstDocId = self.resourceDocumentId(resourceDst)

        result = self.assignmentResourceToResource(resourceSrcDocId, resourceDstDocId)
        if len(result) == 0:
            logger.debug(
                f'[{PolicyRepositoryImpl.revokeAssignmentResourceToResource.__qualname__}] Resource assignment between resource and another resource does not exist, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})')
            raise ResourceAssignmentDoesNotExistException(
                f'Resource assignment between resource and another resource does not exist, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})')
        result = result[0]

        # Delete the document
        aql = '''
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        '''
        bindVars = {"_id": result['_id']}
        logger.debug(
            f'[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Revoke (resource with another resource), source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    def assignmentResourceToResource(self, resourceSrcDocId, resourceDstDocId) -> List:
        aql = '''
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
              RETURN d
        '''
        bindVars = {"fromId": resourceSrcDocId, "toId": resourceDstDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    def connectResourceToOwner(self, resource: Resource, tokenData: TokenData):
        userDocId = self.userDocumentId(User.createFrom(id=tokenData.id(), name=tokenData.name()))
        resourceDocId = self.resourceDocumentId(resource)

        aql = '''
            UPSERT {_from: @fromId, _to: @toId}
                INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
              IN owned_by                  
            '''
        bindVars = {"fromId": resourceDocId, "toId": userDocId, "fromType": resource.type(),
                    "toType": ResourceTypeConstant.USER.value}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        for role in tokenData.roles():
            roleDocId = self.roleDocumentId(Role.createFrom(id=role['id'], name=role['name']))
            aql = '''
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                  IN owned_by                  
                '''
            bindVars = {"fromId": resourceDocId, "toId": roleDocId, "fromType": resource.type(),
                        "toType": ResourceTypeConstant.ROLE.value}
            _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def roleAccessPermissionsData(self, tokenData: TokenData) -> List[RoleAccessPermissionData]:
        rolesConditions = ''
        for role in tokenData.roles():
            if rolesConditions == '':
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'
        aql = '''
                FOR role IN resource
                FILTER (#rolesConditions) AND role.type == 'role'
                LET owned_by = FIRST(FOR v1, e1 IN OUTBOUND role._id `owned_by`
                                    RETURN {"id": v1.id, "type": v1.type})
                LET permissions = (FOR v1, e1 IN OUTBOUND role._id `has`
                                    FILTER e1._from_type == 'role' AND e1._to_type == 'permission'
                                    LET resource_types = (FOR v2, e2 IN OUTBOUND v1._id `for`
                                        RETURN {"id": v2.id, "name": v2.name})
                                    RETURN {"permission": {"id": v1.id, "name": v1.name, "allowed_actions": v1.allowed_actions}, "resource_types": resource_types})
                                
                LET accesses = (FOR v1, e1 IN OUTBOUND role._id `access`
                                    FOR v2, e2, p IN 1..100 OUTBOUND v1._id `has`
                                        RETURN p)
                                
                RETURN {"role": {"id": role.id, "name": role.name}, "owned_by": owned_by, "permissions": permissions, "accesses": accesses}
                    '''
        aql = aql.replace('#rolesConditions', rolesConditions)

        queryResult = self._db.AQLQuery(aql, rawResults=True)
        qResult = queryResult.result
        if len(qResult) == 0:
            return []
        result = []
        for item in qResult:
            ownedByString = '' if item['owned_by'] is None else item['owned_by']['name']
            role = Role.createFrom(id=item['role']['id'], name=item['role']['name'], ownedBy=ownedByString)
            permissions = item['permissions']
            permList = []
            # For each permission
            for permItem in permissions:
                perm = Permission(id=permItem['permission']['id'], name=permItem['permission']['name'],
                                  allowedActions=permItem['permission']['allowed_actions'])
                resList = []
                # Get the resource types for the permission
                for resItem in permItem['resource_types']:
                    resList.append(ResourceType(id=resItem['id'], name=resItem['name']))

                p = PermissionWithResourceTypes(permission=perm, resourceTypes=resList)
                # Add it in the permission list
                permList.append(p)
            ownedBy = None
            if item['owned_by'] is not None:
                ownedBy = Resource(id=item['owned_by']['id'], type=item['owned_by']['type'])
            accessTree = self._fetchAccessTree(accesses=item['accesses'])
            permData = RoleAccessPermissionData(role=role, permissions=permList, ownedBy=ownedBy, accessTree=accessTree)
            result.append(permData)

        return result

    def _fetchAccessTree(self, accesses: List[dict] = None) -> List[AccessNode]:
        if accesses is None:
            return []

        objects:Dict[str, AccessNode] = defaultdict()
        result = []

        for acc in accesses:
            for edge in acc['edges']:
                if edge['_from'] not in objects:
                    self._addAccessKey(result=objects, key=edge['_from'], verts=acc['vertices'])
                    result.append(objects[edge['_from']])
                if edge['_to'] not in objects:
                    self._addAccessKey(result=objects, key=edge['_to'], verts=acc['vertices'])
                if objects[edge['_to']] not in objects[edge['_from']].children:
                    objects[edge['_from']].children.append(objects[edge['_to']])

        return result

    def _addAccessKey(self, result: dict, key: str, verts: List[dict]):
        for vert in verts:
            if vert['_id'] == key:
                node = AccessNode()
                node.resource = Resource(id=vert['id'], type=vert['type'])
                node.resourceName = vert['name']
                result[key] = node
