"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List, Any

from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException import \
    ResourceAssignmentAlreadyExistException
from src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException import \
    ResourceAssignmentDoesNotExistException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
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
            raise Exception(f'[{PolicyRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')

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
            FOR d IN role
                FILTER d.id == @id
                RETURN d
        '''
        bindVars = {"id": role.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise RoleDoesNotExistException(f'role id: {role.id()}')
        result = result[0]
        roleDocId = result['_id']
        return roleDocId

    def userDocumentId(self, user):
        aql = '''
            FOR d IN user
                FILTER d.id == @id
                RETURN d
        '''
        bindVars = {"id": user.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserDoesNotExistException(f'user id: {user.id()}')
        result = result[0]
        userDocId = result['_id']
        return userDocId

    def userGroupDocumentId(self, userGroup):
        aql = '''
            FOR d IN user_group
                FILTER d.id == @id
                RETURN d
        '''
        bindVars = {"id": userGroup.id()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            raise UserGroupDoesNotExistException(f'user group id: {userGroup.id()}')
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
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeRoleFromUser(self, role: Role, user: User) -> None:
        userDocId = self.userDocumentId(user)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUser(roleDocId, userDocId)
        if len(result) == 0:
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
        logger.debug(f'[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] - Revoke role with id: {role.id()} from user with id: {user.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

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
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeRoleFromUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUserGroup(roleDocId, userGroupDocId)
        if len(result) == 0:
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
        logger.debug(f'[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] - Revoke role with id: {role.id()} from user group with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

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
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    def revokeUserFromUserGroup(self, user: User, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        userDocId = self.userDocumentId(user)
        result = self.assignmentUserToUserGroup(userDocId, userGroupDocId)
        if len(result) == 0:
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
        logger.debug(f'[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] - Revoke user with id: {user.id()} from user group with id: {userGroup.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

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

