"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
import pickle
from collections import defaultdict
from typing import List, Any, Dict

from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.permission.Permission import Permission, PermissionAction
from src.domain_model.permission_context.PermissionContext import (
    PermissionContext,
    PermissionContextConstant,
)
from src.domain_model.policy.AccessNode import AccessNode
from src.domain_model.policy.PermissionWithPermissionContexts import (
    PermissionWithPermissionContexts,
)
from src.domain_model.policy.PolicyRepository import PolicyRepository
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.policy.access_node_content.AccessNodeContent import (
    AccessNodeContentTypeConstant,
)
from src.domain_model.policy.access_node_content.ResourceInstanceAccessNodeContent import (
    ResourceInstanceAccessNodeContent,
)
from src.domain_model.policy.model.ProjectIncludesRealmsIncludeUsersIncludeRoles import \
    ProjectIncludesRealmsIncludeUsersIncludeRoles
from src.domain_model.policy.model.RealmIncludesUsersIncludeRoles import RealmIncludesUsersIncludeRoles
from src.domain_model.policy.model.UserIncludesRealmsAndRoles import UserIncludesRealmsAndRoles
from src.domain_model.policy.model.UserIncludesRoles import UserIncludesRoles
from src.domain_model.project.Project import Project
from src.domain_model.realm.Realm import Realm
from src.domain_model.resource.Resource import Resource
from src.domain_model.resource.exception.InvalidResourceException import (
    InvalidResourceException,
)
from src.domain_model.resource.exception.PermissionContextDoesNotExistException import (
    PermissionContextDoesNotExistException,
)
from src.domain_model.resource.exception.PermissionDoesNotExistException import (
    PermissionDoesNotExistException,
)
from src.domain_model.resource.exception.ResourceAssignmentAlreadyExistException import (
    ResourceAssignmentAlreadyExistException,
)
from src.domain_model.resource.exception.ResourceAssignmentDoesNotExistException import (
    ResourceAssignmentDoesNotExistException,
)
from src.domain_model.resource.exception.RoleDoesNotExistException import (
    RoleDoesNotExistException,
)
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.resource.exception.UserDoesNotExistException import (
    UserDoesNotExistException,
)
from src.domain_model.resource.exception.UserGroupDoesNotExistException import (
    UserGroupDoesNotExistException,
)
from src.domain_model.role.Role import Role
from src.domain_model.token.TokenData import TokenData
from src.domain_model.token.TokenService import TokenService
from src.domain_model.user.User import User
from src.domain_model.user_group.UserGroup import UserGroup
from src.port_adapter.repository.cache.RedisCache import RedisCache
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class PolicyRepositoryImpl(PolicyRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
                username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
                password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
            )
            self._db = self._connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "")]
        except Exception as e:
            logger.warn(
                f"[{PolicyRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}"
            )
            raise Exception(f"Could not connect to the db, message: {e}")

        try:
            import src.port_adapter.AppDi as AppDi

            cache = AppDi.instance.get(RedisCache)
            self._cache = cache.client()
            self._cacheRolesTreesKeyPrefix = cache.rolesTreesKeyPrefix()
        except Exception as e:
            raise Exception(
                f"[{PolicyRepositoryImpl.__init__.__qualname__}] Could not connect to the redis, message: {e}"
            )

    @debugLogger
    def persistRolesTreesCache(self, rolesTrees: List[RoleAccessPermissionData], token: str, ttl: int = -1) -> None:
        pickled = pickle.dumps(rolesTrees)
        self._cache.setex(f"{self._cacheRolesTreesKeyPrefix}{token}", ttl, pickled)

    @debugLogger
    def rolesTreesInCacheExists(self, token: str) -> bool:
        return self._cache.exists(f"{self._cacheRolesTreesKeyPrefix}{token}") == 1

    @debugLogger
    def getRolesTreesFromCache(self, token: str) -> List[RoleAccessPermissionData]:
        return pickle.loads(self._cache.get(f"{self._cacheRolesTreesKeyPrefix}{token}"))

    @debugLogger
    def deleteRolesTreesCache(self) -> None:
        generator = self._cache.scan_iter(f"{self._cacheRolesTreesKeyPrefix}*")
        listKeys = list(generator)
        for key in listKeys:
            self._cache.delete(key)

    @debugLogger
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

    @debugLogger
    def roleDocumentId(self, role: Role):
        # Get the role doc id
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'role'
                RETURN d
        """
        bindVars = {"id": role.id()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.roleDocumentId.__qualname__}] role id: {role.id()}"
            )
            raise RoleDoesNotExistException(f"role id: {role.id()}")
        result = result[0]
        roleDocId = result["_id"]
        return roleDocId

    @debugLogger
    def userDocumentId(self, user: User):
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                RETURN d
        """
        bindVars = {"id": user.id()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.userDocumentId.__qualname__}] user id: {user.id()}"
            )
            raise UserDoesNotExistException(f"user id: {user.id()}")
        result = result[0]
        userDocId = result["_id"]
        return userDocId

    @debugLogger
    def userGroupDocumentId(self, userGroup: UserGroup):
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user_group'
                RETURN d
        """
        bindVars = {"id": userGroup.id()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.userGroupDocumentId.__qualname__}] user group id: {userGroup.id()}"
            )
            raise UserGroupDoesNotExistException(f"user group id: {userGroup.id()}")
        result = result[0]
        userDocId = result["_id"]
        return userDocId

    # region Assignment Role - User
    @debugLogger
    def assignRoleToUser(self, role: Role, user: User) -> None:
        userDocId = self.userDocumentId(user)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.assignmentRoleToUser(roleDocId, userDocId)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignRoleToUser.__qualname__}] Resource already assigned for user: {user.id()}, role: {role.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned for user: {user.id()}, role: {role.id()}"
            )

        # Assign a role to the user
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user', _to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user', _to_type: 'role'}
                  IN has                  
                """
        bindVars = {"fromId": userDocId, "toId": roleDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def revokeRoleFromUser(self, role: Role, user: User) -> None:
        userDocId = self.userDocumentId(user)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUser(roleDocId, userDocId)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Resource assignment for user: {user.id()} and role: {role.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for user: {user.id()} and role: {role.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        """
        bindVars = {"_id": result["_id"]}
        logger.debug(
            f"[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Revoke role with id: {role.id()} from user with id: {user.id()}"
        )
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        _ = queryResult.result

        self.deleteRolesTreesCache()

    @debugLogger
    def assignmentRoleToUser(self, roleDocId, userDocId) -> List:
        # Check if there is a link
        aql = """
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d._from_type == 'user' AND d._to_type == 'role'
              RETURN d
        """
        bindVars = {"fromId": userDocId, "toId": roleDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment Role - User Group
    @debugLogger
    def assignRoleToUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.assignmentRoleToUserGroup(roleDocId, userGroupDocId)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignRoleToUserGroup.__qualname__}] Resource already assigned for user group: {userGroup.id()}, role: {role.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned for user group: {userGroup.id()}, role: {role.id()}"
            )

        # Assign a role to the user group
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'role'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'role'}
                  IN has                  
                """
        bindVars = {"fromId": userGroupDocId, "toId": roleDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def revokeRoleFromUserGroup(self, role: Role, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        roleDocId = self.roleDocumentId(role)
        result = self.assignmentRoleToUserGroup(roleDocId, userGroupDocId)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Resource assignment for user group: {userGroup.id()} and role: {role.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for user group: {userGroup.id()} and role: {role.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        """
        bindVars = {"_id": result["_id"]}
        logger.debug(
            f"[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke role with id: {role.id()} from user group with id: {userGroup.id()}"
        )
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        _ = queryResult.result

        self.deleteRolesTreesCache()

    @debugLogger
    def assignmentRoleToUserGroup(self, roleDocId, userGroupDocId) -> List:
        # Check if there is a link
        aql = """
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d._from_type == 'user_group' AND d._to_type == 'role'
              RETURN d
        """
        bindVars = {"fromId": userGroupDocId, "toId": roleDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment User - User Group
    @debugLogger
    def assignUserToUserGroup(self, user: User, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        userDocId = self.userDocumentId(user)

        # Check if there is any already exist link?
        result = self.assignmentUserToUserGroup(userDocId, userGroupDocId)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignUserToUserGroup.__qualname__}] Resource already assigned for user group: {userGroup.id()}, user: {user.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned for user group: {userGroup.id()}, user: {user.id()}"
            )

        # Assign a user to the user group
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'user'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'user_group', _to_type: 'user'}
                  IN has                  
                """
        bindVars = {"fromId": userGroupDocId, "toId": userDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def revokeUserFromUserGroup(self, user: User, userGroup: UserGroup) -> None:
        userGroupDocId = self.userGroupDocumentId(userGroup)
        userDocId = self.userDocumentId(user)
        result = self.assignmentUserToUserGroup(userDocId, userGroupDocId)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Resource assignment for user group: {userGroup.id()} and user: {user.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for user group: {userGroup.id()} and user: {user.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        """
        bindVars = {"_id": result["_id"]}
        logger.debug(
            f"[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Revoke user with id: {user.id()} from user group with id: {userGroup.id()}"
        )
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        _ = queryResult.result

        self.deleteRolesTreesCache()

    @debugLogger
    def assignmentUserToUserGroup(self, userDocId, userGroupDocId) -> List:
        # Check if there is a link
        aql = """
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d._from_type == 'user_group' AND d._to_type == 'user'
              RETURN d
        """
        bindVars = {"fromId": userGroupDocId, "toId": userDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    # region Assignment Role - Permission - Permission Context
    @debugLogger
    def assignRoleToPermission(self, role: Role, permission: Permission) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermission(roleDocId, permissionDocId)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignRoleToPermission.__qualname__}] Resource already assigned role id: {role.id()}, permission: {permission.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned role id: {role.id()}, permission: {permission.id()}"
            )

        # Assign the role to the permission
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: 'permission'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: 'permission'}
                  IN `has`                  
                """
        bindVars = {"fromId": roleDocId, "toId": permissionDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def permissionDocumentId(self, permission: Permission):
        # Get the doc id
        aql = """
            FOR d IN permission
                FILTER d.id == @id
                RETURN d
        """
        bindVars = {"id": permission.id()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.permissionDocumentId.__qualname__}] permission id: {permission.id()}"
            )
            raise PermissionDoesNotExistException(f"permission id: {permission.id()}")
        result = result[0]
        docId = result["_id"]
        return docId

    @debugLogger
    def permissionContextDocumentId(self, permissionContext: PermissionContext):
        # Get the doc id
        aql = """
            FOR d IN permission_context
                FILTER d.id == @id
                RETURN d
        """
        bindVars = {"id": permissionContext.id()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.permissionContextDocumentId.__qualname__}] permission context id: {permissionContext.id()}"
            )
            raise PermissionContextDoesNotExistException(
                f"permission context id: {permissionContext.id()}"
            )
        result = result[0]
        docId = result["_id"]
        return docId

    @debugLogger
    def assignmentRoleToPermission(self, roleDocId, permissionDocId) -> List:
        # Check if there is a link
        aql = """
            WITH `has`, `for`, `resource`
            FOR d IN `resource`
                FILTER d._id == @roleDocId AND d.type == 'role'
                LET r = (
                    FOR v1,e1 IN OUTBOUND d._id `has` FILTER e1._to_type == "permission" AND v1._id == @permissionDocId
                        RETURN  {"permission": v1, "to_permission_edge": e1}
                )
                FILTER LENGTH(r) > 0
                RETURN {"role": d, "permission": r}
        """
        bindVars = {"roleDocId": roleDocId, "permissionDocId": permissionDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    @debugLogger
    def revokeRoleToPermissionAssignment(
        self, role: Role, permission: Permission
    ) -> None:
        roleDocId = self.roleDocumentId(role)
        permissionDocId = self.permissionDocumentId(permission)

        # Check if there is any already exist link?
        result = self.assignmentRoleToPermission(roleDocId, permissionDocId)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeRoleToPermissionAssignment.__qualname__}] Resource not exist for assignment a role id: {role.id()} to permission id: {permission.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for role id: {role.id()}, permission id: {permission.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        """
        for d in result["permission"]:
            bindVars = {"_id": d["to_permission_edge"]["_id"]}
            queryResult: AQLQuery = self._db.AQLQuery(
                aql, bindVars=bindVars, rawResults=True
            )
            _ = queryResult.result

        self.deleteRolesTreesCache()

        logger.debug(
            f"[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke assignment of role with id: {role.id()} to permission with id: {permission.id()}"
        )

    @debugLogger
    def bulkAssignPermissionToPermissionContext(self, objList: List[dict]):
        actionFunction = """
                    function (params) {                                            
                        let db = require('@arangodb').db;
                        let objList = params['permissionAndPermissionContextIdList'];
                        for (let index in objList) {
                            let res = db.for.byExample({_from: `permission/${objList[index].permission_id}`,
                                                       _to: `permission_context/${objList[index].permission_context_id}`}).toArray();
                            if (res.length == 0) {
                                db.for.insert({
                                    _from_type: "permission",
                                    _to_type: "permission_context",
                                    _from: `permission/${objList[index].permission_id}`,
                                    _to: `permission_context/${objList[index].permission_context_id}`
                                }, {"overwrite": true});
                            }
                        }
                    }
                """
        params = {
            "permissionAndPermissionContextIdList": list(map(lambda obj: {
                "permission_id": obj['permission'].id(),
                "permission_context_id": obj['permission_context'].id()
            }, objList))
        }
        self._db.transaction(
            collections={"write": ["for"]},
            action=actionFunction,
            params=params,
        )

    @debugLogger
    def bulkRemovePermissionToPermissionContextAssignment(self, objList: List[dict]):
        actionFunction = """
                    function (params) {                                            
                        let db = require('@arangodb').db;
                        let objList = params['permissionAndPermissionContextIdList'];
                        for (let index in objList) {
                            db.for.removeByExample({_from: `permission/${objList[index].permission_id}`,
                                                       _to: `permission_context/${objList[index].permission_context_id}`});                            
                        }
                    }
                """
        params = {
            "permissionAndPermissionContextIdList": list(map(lambda obj: {
                "permission_id": obj['permission'].id(),
                "permission_context_id": obj['permission_context'].id()
            }, objList))
        }
        self._db.transaction(
            collections={"write": ["for"]},
            action=actionFunction,
            params=params,
        )

    @debugLogger
    def bulkAssignRoleToPermission(self, objList: List[dict]):
        actionFunction = """
                        function (params) {                                            
                            let db = require('@arangodb').db;
                            let objList = params['roleAndPermissionIdList'];
                            for (let index in objList) {
                                let res = db.has.byExample({_from: `resource/${objList[index].role_id}`,
                                                           _to: `permission/${objList[index].permission_id}`}).toArray();
                                if (res.length == 0) {
                                    db.has.insert({
                                        _from_type: "role",
                                        _to_type: "permission",
                                        _from: `resource/${objList[index].role_id}`,
                                        _to: `permission/${objList[index].permission_id}`
                                    }, {"overwrite": true});
                                }
                            }
                        }
                    """
        params = {
            "roleAndPermissionIdList": list(map(lambda obj: {
                "role_id": obj['role'].id(),
                "permission_id": obj['permission'].id()
            }, objList))
        }
        self._db.transaction(
            collections={"write": ["has"]},
            action=actionFunction,
            params=params,
        )

    @debugLogger
    def assignPermissionToPermissionContext(
        self, permission: Permission, permissionContext: PermissionContext
    ) -> None:
        permissionDocId = self.permissionDocumentId(permission)
        permissionContextDocId = self.permissionContextDocumentId(permissionContext)

        # Check if there is any link that exists already?
        result = self.assignmentPermissionToPermissionContext(
            permissionDocId, permissionContextDocId
        )
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignPermissionToPermissionContext.__qualname__}] Resource already assigned permission: {permission.id()}, permission context id: {permissionContext.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned permission: {permission.id()}, permission context id: {permissionContext.id()}"
            )

        # Assign the permission to permission context
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'permission', _to_type: 'permission_context'}
                  IN `for`                  
                """
        bindVars = {"fromId": permissionDocId, "toId": permissionContextDocId}
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def assignmentPermissionToPermissionContext(
        self, permissionDocId, permissionContextDocId
    ) -> List:
        # Check if there is a link
        aql = """
            WITH `for`, `permission`
            FOR d IN `permission`
                FILTER d._id == @permissionDocId
                LET r = (
                    FOR v1,e1 IN OUTBOUND d._id `for` FILTER e1._to_type == "permission_context" AND v1._id == @permissionContextDocId
                        RETURN  {"permission_context": v1, "to_permission_context_edge": e1}
                )
                FILTER LENGTH(r) > 0
                RETURN {"permission": d, "permission_context": r}
        """
        bindVars = {
            "permissionDocId": permissionDocId,
            "permissionContextDocId": permissionContextDocId,
        }
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    @debugLogger
    def revokePermissionToPermissionContextAssignment(
        self, permission: Permission, permissionContext: PermissionContext
    ) -> None:
        permissionDocId = self.permissionDocumentId(permission)
        permissionContextDocId = self.permissionContextDocumentId(permissionContext)

        # Check if there is any already existing link?
        result = self.assignmentPermissionToPermissionContext(
            permissionDocId, permissionContextDocId
        )
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokePermissionToPermissionContextAssignment.__qualname__}] Resource assignment for permission id: {permission.id()}, permission context id: {permissionContext.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for permission id: {permission.id()}, permission context id: {permissionContext.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN `for`
                FILTER d._id == @_id
                REMOVE d IN `for`
        """
        for d in result["permission_context"]:
            bindVars = {"_id": d["to_permission_context_edge"]["_id"]}
            queryResult: AQLQuery = self._db.AQLQuery(
                aql, bindVars=bindVars, rawResults=True
            )
            _ = queryResult.result

        self.deleteRolesTreesCache()

        logger.debug(
            f"[{PolicyRepositoryImpl.revokeRoleFromUserGroup.__qualname__}] Revoke assignment permission with id: {permission.id()} to permission context with id: {permissionContext.id()}"
        )

    # endregion

    # region Access Role - Resource
    @debugLogger
    def grantAccessRoleToResource(self, role: Role, resource: Resource) -> None:
        resourceDocId = self.resourceDocumentId(resource)
        roleDocId = self.roleDocumentId(role)

        # Check if there is any already exist link?
        result = self.accessRoleToResource(roleDocId, resourceDocId, resource)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.grantAccessRoleToResource.__qualname__}] Resource already assigned for role: {role.id()}, resource: {resource.id()}"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned for role: {role.id()}, resource: {resource.id()}"
            )

        # Assign a role to the user
        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: @permissionContextName}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: 'role', _to_type: @permissionContextName}
                  IN access                  
                """
        bindVars = {
            "fromId": roleDocId,
            "toId": resourceDocId,
            "permissionContextName": resource.type(),
        }
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def revokeRoleToResourceAccess(self, role: Role, resource: Resource) -> None:
        resourceDocId = self.resourceDocumentId(resource)
        roleDocId = self.roleDocumentId(role)
        result = self.accessRoleToResource(roleDocId, resourceDocId, resource)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeRoleToResourceAccess.__qualname__}] Resource assignment for role: {role.id()} and resource: {resource.id()}"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment for role: {role.id()} and resource: {resource.id()}"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN `access`
                FILTER d._id == @_id
                REMOVE d IN `access`
        """
        bindVars = {"_id": result["_id"]}
        logger.debug(
            f"[{PolicyRepositoryImpl.revokeRoleFromUser.__qualname__}] Revoke role with id: {role.id()} from resource with id: {resource.id()}, type: {resource.type()}"
        )
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        _ = queryResult.result

        self.deleteRolesTreesCache()

    @debugLogger
    def accessRoleToResource(
        self, roleDocId, resourceDocId, resource: Resource
    ) -> List:
        # Check if there is a link
        aql = """
            FOR d IN access
              FILTER 
                d._from == @fromId AND d._to == @toId
                AND d._from_type == 'role' AND d._to_type == @permissionContextName
              RETURN d
        """
        bindVars = {
            "fromId": roleDocId,
            "toId": resourceDocId,
            "permissionContextName": resource.type(),
        }
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    @debugLogger
    def resourceDocumentId(self, resource: Resource):
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == @type
                RETURN d
        """
        bindVars = {"id": resource.id(), "type": resource.type()}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.resourceDocumentId.__qualname__}] resource id: {resource.id()}"
            )
            raise RoleDoesNotExistException(f"resource id: {resource.id()}")
        result = result[0]
        docId = result["_id"]
        return docId

    # endregion

    # region Assignment Resource - Resource
    @debugLogger
    def assignResourceToResource(
        self, resourceSrc: Resource, resourceDst: Resource
    ) -> None:
        resourceSrcDocId = self.resourceDocumentId(resourceSrc)
        resourceDstDocId = self.resourceDocumentId(resourceDst)

        # Check if there is any already exist link?
        result = self.assignmentResourceToResource(resourceSrcDocId, resourceDstDocId)
        if len(result) > 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.assignResourceToResource.__qualname__}] Resource already assigned, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})"
            )
            raise ResourceAssignmentAlreadyExistException(
                f"Resource already assigned, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})"
            )

        aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                  IN has                  
                """
        bindVars = {
            "fromId": resourceSrcDocId,
            "toId": resourceDstDocId,
            "fromType": resourceSrc.type(),
            "toType": resourceDst.type(),
        }
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        self.deleteRolesTreesCache()

    @debugLogger
    def revokeAssignmentResourceToResource(
        self, resourceSrc: Resource, resourceDst: Resource
    ) -> None:
        resourceSrcDocId = self.resourceDocumentId(resourceSrc)
        resourceDstDocId = self.resourceDocumentId(resourceDst)

        result = self.assignmentResourceToResource(resourceSrcDocId, resourceDstDocId)
        if len(result) == 0:
            logger.debug(
                f"[{PolicyRepositoryImpl.revokeAssignmentResourceToResource.__qualname__}] Resource assignment between resource and another resource does not exist, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})"
            )
            raise ResourceAssignmentDoesNotExistException(
                f"Resource assignment between resource and another resource does not exist, source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})"
            )
        result = result[0]

        # Delete the document
        aql = """
            FOR d IN has
                FILTER d._id == @_id
                REMOVE d IN has
        """
        bindVars = {"_id": result["_id"]}
        logger.debug(
            f"[{PolicyRepositoryImpl.revokeUserFromUserGroup.__qualname__}] Revoke (resource with another resource), source resource (id, type): ({resourceSrc.id()}, {resourceSrc.type()}), destination resource (id, type): ({resourceDst.id()}, {resourceDst.type()})"
        )
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        _ = queryResult.result

        self.deleteRolesTreesCache()

    @debugLogger
    def assignmentResourceToResource(self, resourceSrcDocId, resourceDstDocId) -> List:
        aql = """
            FOR d IN has
              FILTER 
                d._from == @fromId AND d._to == @toId
              RETURN d
        """
        bindVars = {"fromId": resourceSrcDocId, "toId": resourceDstDocId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result

        return result

    # endregion

    @debugLogger
    def permissionsByTokenData(
        self,
        tokenData: TokenData = None,
        roleAccessPermissionData: List[RoleAccessPermissionData] = None,
        sortData: str = "",
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData) or \
                self._canRead(roleAccessPermissionData, PermissionContextConstant.PERMISSION):
            aql = """
                LET ds = (FOR d IN permission #sortData RETURN d)
                RETURN {items: ds}
            """
            if sortData != "":
                aql = aql.replace("#sortData", f"SORT {sortData}")
            else:
                aql = aql.replace("#sortData", "")

            queryResult = self._db.AQLQuery(aql, rawResults=True)
            return queryResult.result[0]

    @debugLogger
    def permissionContextsByTokenData(
        self,
        tokenData: TokenData = None,
        roleAccessPermissionData: List[RoleAccessPermissionData] = None,
        sortData: str = "",
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData) or \
                self._canRead(roleAccessPermissionData, PermissionContextConstant.PERMISSION_CONTEXT):
            aql = """
                LET ds = (FOR d IN permission_context #sortData RETURN d)
                RETURN {items: ds}
            """
            if sortData != "":
                aql = aql.replace("#sortData", f"SORT {sortData}")
            else:
                aql = aql.replace("#sortData", "")

            queryResult = self._db.AQLQuery(aql, rawResults=True)
            return queryResult.result[0]

    @debugLogger
    def _canRead(
        self,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        permissionContext: PermissionContextConstant,
    ):
        for roleAccessPermission in roleAccessPermissionData:
            for permissionWithContexts in roleAccessPermission.permissions:
                if (
                    PermissionAction.READ.value
                    in permissionWithContexts.permission.allowedActions()
                    and PermissionAction.READ.value
                    not in permissionWithContexts.permission.deniedActions()
                ):
                    for context in permissionWithContexts.permissionContexts:
                        if context.type() == permissionContext.value:
                            return True

    @debugLogger
    def rolesTrees(
        self,
        token: str = "",
        tokenData: TokenData = None,
        roleAccessPermissionDataList: List[RoleAccessPermissionData] = None,
    ) -> List[RoleAccessPermissionData]:
        roles = tokenData.roles()
        doFilter = False
        if self.rolesTreesInCacheExists(token=token):
            return self.getRolesTreesFromCache(token=token)
        else:
            rolesTrees = self.getRolesTrees(
                roles=roles,
                doFilter=doFilter,
                roleAccessPermissionDataList=roleAccessPermissionDataList,
                tokenData=tokenData)

            self.persistRolesTreesCache(rolesTrees=rolesTrees, token=token, ttl=int(os.getenv("CAFM_IDENTITY_ROLES_TREES_TTL_IN_SECONDS", 300)))

            return rolesTrees

    @debugLogger
    def getRolesTrees(self, roles, doFilter, roleAccessPermissionDataList, tokenData):
        if TokenService.isSuperAdmin(
            tokenData=tokenData
        ) or TokenService.isSysAdmin(
            tokenData=tokenData
        ) or self._hasReadAllRolesTreesInPermissionContext(
            roleAccessPermissionDataList
        ):
            aql = """
                LET ds = (FOR d IN resource FILTER d.type == 'role' RETURN d)
                RETURN {items: ds}
            """

            queryResult = self._db.AQLQuery(aql, rawResults=True)
            roles = queryResult.result[0]["items"]

        return self._roleTreeListOf(roles, roleAccessPermissionDataList, doFilter)

    @debugLogger
    def roleTree(
        self,
        tokenData: TokenData = None,
        roleId: str = "",
        roleAccessPermissionData: List[RoleAccessPermissionData] = None,
    ) -> RoleAccessPermissionData:
        roles = tokenData.roles()
        hasRoleInRoles = False
        for r in roles:
            if r["id"] == roleId:
                hasRoleInRoles = True
        doFilter = True
        roleList = None
        if TokenService.isSuperAdmin(
            tokenData=tokenData
        ) or TokenService.isSysAdmin(
            tokenData=tokenData
        ) or self._hasReadAllRolesTreesInPermissionContext(roleAccessPermissionData):
            roleList = self._roleById(roleId)
            doFilter = False
        else:
            if not hasRoleInRoles:
                raise UnAuthorizedException()
            roleList = self._roleById(roleId)

        result = self._roleTreeListOf(roleList, roleAccessPermissionData, doFilter)
        if len(result) > 0:
            return result[0]
        else:
            return None

    @debugLogger
    def _roleById(self, roleId):
        aql = """
                LET ds = (FOR d IN resource FILTER d.type == 'role' AND d.id == @id RETURN d)
                RETURN {items: ds}
              """
        bindVars = {"id": roleId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        return queryResult.result[0]["items"]

    @debugLogger
    def _hasReadAllRolesTreesInPermissionContext(
        self, roleAccessPermissionData: List[RoleAccessPermissionData]
    ) -> bool:
        for roleAccessPermission in roleAccessPermissionData:
            for permissionWithContext in roleAccessPermission.permissions:
                if (
                    PermissionAction.READ.value
                    in permissionWithContext.permission.allowedActions()
                    and PermissionAction.READ.value
                    not in permissionWithContext.permission.deniedActions()
                ):
                    for permissionContext in permissionWithContext.permissionContexts:
                        if (
                            permissionContext.type()
                            == PermissionContextConstant.ALL_ROLES_TREES.value
                        ):
                            return True
        return False

    @debugLogger
    def _roleTreeListOf(
        self,
        roles: List[dict],
        roleAccessPermissionDataList: List[RoleAccessPermissionData],
        doFilter,
    ) -> List[RoleAccessPermissionData]:
        if doFilter:
            resultItems = self._filterRoleAccessPermissionDataItems(
                roleAccessPermissionDataList
            )
        else:
            rawDataItems = self._rawRoleTreeItems(roles, True)
            resultItems = self._constructRoleAccessPermissionDataFromRawRoleTreeItems(
                rawDataItems
            )

        return resultItems

    @debugLogger
    def resourcesOfTypeByConnectedResourceId(self, resourceType: str = "",
                                             resourceId: str = "",
                                             tokenData: TokenData = None,
                                             roleAccessPermissionData: List[RoleAccessPermissionData] = None,
                                             sortData: str = "",
                                             ):
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                FOR d IN resource
                    FILTER d.id == @resource_id
                    FOR v IN 1..100 OUTBOUND d._id `has` FILTER v.type == @type #sortData RETURN v
            """
            if sortData != "":
                aql = aql.replace("#sortData", f"SORT {sortData}")
            else:
                aql = aql.replace("#sortData", "")

            bindVars = {"type": resourceType, "resource_id": resourceId}
            queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            return {"items": result if len(result) > 0 else [], "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                RETURN MERGE(FOR role IN resource
                    FILTER (#rolesConditions) AND role.type == 'role'
                    LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.id == @resource_id RETURN v1)
                    LET accesses = (FOR v1 IN 1..100 OUTBOUND role._id `access`
                                        FOR v2 IN 1..100 OUTBOUND v1._id `has`
                                        FILTER v2.id == @resource_id
                                            RETURN v2
                                    )
                    LET owned_resources = (FOR v1 IN INBOUND role._id `owned_by` FILTER v1.id == @resource_id RETURN v1)
                    LET result_unique = UNION_DISTINCT(owned_resources, accesses, direct_access)
                    LET result = LENGTH(FLATTEN(result_unique)) > 0 ? 
                        (FOR d IN resource FILTER d.id == @resource_id FOR v IN 1..100 OUTBOUND d._id `has` FILTER v.type == @type RETURN v)
                    : (RETURN [])
                    
                    LET sorted_result = (FOR d IN result #sortData RETURN d)
                    RETURN sorted_result)
                        """
        if sortData != "":
            aql = aql.replace("#sortData", f"SORT {sortData}")
        else:
            aql = aql.replace("#sortData", "")
        aql = aql.replace("#rolesConditions", rolesConditions)
        bindVars = {"type": resourceType, "resource_id": resourceId}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result[0] if queryResult.result != [] else []

        if not result:
            filteredItems = self._filterItems(
                [], roleAccessPermissionData, resourceType
            )
        else:
            filteredItems = self._filterItems(
                result, roleAccessPermissionData, resourceType
            )
        return {"items": filteredItems, "totalItemCount": len(filteredItems)}


    @debugLogger
    def resourcesOfTypeByTokenData(
        self,
        resourceType: str = "",
        tokenData: TokenData = None,
        roleAccessPermissionData: List[RoleAccessPermissionData] = None,
        sortData: str = "",
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                LET ds = (FOR d IN resource FILTER d.type == @type #sortData RETURN d)
                RETURN {items: ds}
            """
            if sortData != "":
                aql = aql.replace("#sortData", f"SORT {sortData}")
            else:
                aql = aql.replace("#sortData", "")

            bindVars = {"type": resourceType}
            queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            return queryResult.result[0]

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                LET resource_user_id = "#userId"
                RETURN MERGE(FOR role IN resource
                    FILTER (#rolesConditions) AND role.type == 'role'
                    LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == @type RETURN v1)
                    LET accesses = (FOR v1 IN OUTBOUND role._id `access`
                                                    FOR v2, e2, p IN 1..100 OUTBOUND v1._id `has`
                                                    FILTER v2.type == @type
                                                        RETURN v2
                                               )
                    LET owned_resources = (FOR v1 IN INBOUND resource_user_id `owned_by` FILTER v1.type == @type RETURN v1)
                    LET result = UNION_DISTINCT(owned_resources, accesses, direct_access)
                    LET sorted_result = (FOR d IN result #sortData RETURN d)
                    RETURN {items: sorted_result})
                """
        if sortData != "":
            aql = aql.replace("#sortData", f"SORT {sortData}")
        else:
            aql = aql.replace("#sortData", "")
        aql = aql.replace("#rolesConditions", rolesConditions)
        aql = aql.replace("#userId", f'resource/{tokenData.id()}')
        bindVars = {"type": resourceType}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result[0] if queryResult.result != [] else []

        if not result:
            filteredItems = self._filterItems(
                [], roleAccessPermissionData, resourceType
            )
        else:
            filteredItems = self._filterItems(
                result["items"], roleAccessPermissionData, resourceType
            )
        return {"items": filteredItems, "totalItemCount": len(filteredItems)}

    @debugLogger
    def realmsByType(
            self,
            tokenData: TokenData = None,
            roleAccessPermissionData: List[RoleAccessPermissionData] = None,
            sortData: str = "",
            realmType: str = None
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                    LET ds = (FOR d IN resource FILTER d.type == "realm" AND d.realm_type == @type #sortData RETURN d)
                    RETURN {items: ds}
                """
            if sortData != "":
                aql = aql.replace("#sortData", f"SORT {sortData}")
            else:
                aql = aql.replace("#sortData", "")

            bindVars = {"type": realmType}
            queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            return queryResult.result[0]

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                    FOR role IN resource
                        FILTER (#rolesConditions) AND role.type == 'role'
                        LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm" AND v1.realm_type == @type RETURN v1)
                        LET accesses = (FOR v1 IN OUTBOUND role._id `access`
                                                        FOR v2, e2, p IN 1..100 OUTBOUND v1._id `has`
                                                        FILTER v2.type == "realm" AND v2.realm_type == @type
                                                            RETURN v2
                                                   )
                        LET owned_resources = (FOR v1 IN INBOUND role._id `owned_by` FILTER v1.type == "realm" AND v1.realm_type == @type RETURN v1)
                        LET result = UNION_DISTINCT(owned_resources, accesses, direct_access)
                        LET sorted_result = (FOR d IN result #sortData RETURN d)
                        RETURN {items: sorted_result}
                    """
        if sortData != "":
            aql = aql.replace("#sortData", f"SORT {sortData}")
        else:
            aql = aql.replace("#sortData", "")
        aql = aql.replace("#rolesConditions", rolesConditions)
        bindVars = {"type": realmType}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result[0] if queryResult.result != [] else []

        if not result:
            filteredItems = self._filterItems(
                [], roleAccessPermissionData, "realm"
            )
        else:
            filteredItems = self._filterItems(
                result["items"], roleAccessPermissionData, "realm"
            )
        return {"items": filteredItems, "totalItemCount": len(filteredItems)}







# region User with Role
    @debugLogger
    def usersIncludeAccessRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                    LET users_with_roles = (FOR user IN resource
                                            FILTER user.type == "user"
                                            FOR role_item IN OUTBOUND user `has`
                                            FILTER role_item.type == "role"
                                            COLLECT user_item = user into groups = role_item
                                                RETURN MERGE(user_item, {roles: groups}))
                    RETURN users_with_roles
                """
            queryResult = self._db.AQLQuery(aql, rawResults=True)
            result = queryResult.result[0]
            return {"items": [self._userIncludesRolesByResultItem(x) for x in result], "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                LET res1 =UNIQUE(FLATTEN(
                            FOR role IN resource
                                FILTER (#rolesConditions)
                                LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == 'realm'
                                            FOR v2 IN INBOUND v1._id `access` FILTER v2.type == "role" RETURN v2)
                                LET accesses = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm"
                                                    FOR v2 IN 1..100 OUTBOUND v1._id `has` FILTER v2.type == "realm"
                                                        FOR v3 IN INBOUND v2._id `access` FILTER v3.type == "role"
                                                                    RETURN v3
                                                           )
                                LET roles = UNION_DISTINCT(accesses, direct_access)
                                RETURN roles
                            ))
                
                
                LET users_with_roles = (FOR user IN resource
                        FILTER user.type == "user"
                        FOR role2 IN res1
                            FILTER role2.type == "role"
                            FOR role3 IN OUTBOUND user `has`
                            FILTER role3.id == role2.id
                            COLLECT user_item = user into groups = role3
                                RETURN MERGE(user_item, {roles: groups}))
                RETURN users_with_roles
                    """
        aql = aql.replace("#rolesConditions", rolesConditions)
        queryResult = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result[0]
        return {"items": [self._userIncludesRolesByResultItem(x) for x in result], "totalItemCount": len(result)}

    @debugLogger
    def usersIncludeRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                        LET users_with_roles = (FOR user IN resource
                                                FILTER user.type == "user"
                                                FOR role_item IN OUTBOUND user `has`
                                                FILTER role_item.type == "role"
                                                COLLECT user_item = user into groups = role_item
                                                    RETURN MERGE(user_item, {roles: groups}))
                        RETURN users_with_roles
                    """
            queryResult = self._db.AQLQuery(aql, rawResults=True)
            result = queryResult.result[0]
            return {"items": [self._userIncludesRolesByResultItem(x) for x in result], "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                    LET res1 =UNIQUE(FLATTEN(
                                FOR role IN resource
                                    FILTER (#rolesConditions)
                                    LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == 'realm'
                                                FOR v2 IN INBOUND v1._id `access` FILTER v2.type == "role" RETURN v2)
                                    LET accesses = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm"
                                                        FOR v2 IN 1..100 OUTBOUND v1._id `has` FILTER v2.type == "realm"
                                                            FOR v3 IN INBOUND v2._id `access` FILTER v3.type == "role"
                                                                        RETURN v3
                                                               )
                                    LET roles = UNION_DISTINCT(accesses, direct_access)
                                    RETURN roles
                                ))

                    LET users_with_roles = (
                        FOR user IN resource
                            FILTER user.type == "user"
                            FOR role2 IN res1
                                FILTER role2.type == "role"
                                FOR role3 IN OUTBOUND user `has`
                                FILTER role3.id == role2.id
                                FOR role4 IN OUTBOUND user `has`
                                    FILTER role4.type == "role"
                                    COLLECT user_item = user into groups = role4
                                        RETURN MERGE(user_item, {roles: unique(groups)}))
                    RETURN users_with_roles
                        """
        aql = aql.replace("#rolesConditions", rolesConditions)
        queryResult = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result[0]
        return {"items": [self._userIncludesRolesByResultItem(x) for x in result], "totalItemCount": len(result)}




    @debugLogger
    def realmsIncludeUsersIncludeRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                            LET users_include_roles = (FOR user IN resource
                                                    FILTER user.type == "user"
                                                    FOR role_item IN OUTBOUND user `has`
                                                    FILTER role_item.type == "role"
                                                    COLLECT user_item = user into groups = role_item
                                                        RETURN MERGE(user_item, {roles: groups}))
                            FOR item IN users_include_roles
                                FOR role2 IN item.roles
                                    FOR realm IN outbound role2 `access`
                                        FILTER realm.type == "realm"
                                        COLLECT realm_item = realm INTO groups = item
                                            RETURN MERGE(realm_item, {users_include_roles: groups})
                        """
            queryResult = self._db.AQLQuery(aql, rawResults=True)
            result = queryResult.result
            return {"items": [self._realmIncludesUsersIncludeRolesByResultItem(x) for x in result],
                    "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                        LET res1 =UNIQUE(FLATTEN(
                                    FOR role IN resource
                                        FILTER (#rolesConditions)
                                        LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == 'realm'
                                                    FOR v2 IN INBOUND v1._id `access` FILTER v2.type == "role" RETURN v2)
                                        LET accesses = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm"
                                                            FOR v2 IN 1..100 OUTBOUND v1._id `has` FILTER v2.type == "realm"
                                                                FOR v3 IN INBOUND v2._id `access` FILTER v3.type == "role"
                                                                            RETURN v3
                                                                   )
                                        LET roles = UNION_DISTINCT(accesses, direct_access)
                                        RETURN roles
                                    ))

                        LET users_with_roles = (
                            FOR user IN resource
                                FILTER user.type == "user"
                                FOR role2 IN res1
                                    FILTER role2.type == "role"
                                    FOR role3 IN OUTBOUND user `has`
                                    FILTER role3.id == role2.id
                                    FOR role4 IN OUTBOUND user `has`
                                        FILTER role4.type == "role"
                                        COLLECT user_item = user into groups = role4
                                            RETURN MERGE(user_item, {roles: unique(groups)}))
                        
                        FOR item IN users_with_roles
                            FOR role2 IN item.roles
                                FOR realm IN outbound role2 `access`
                                    FILTER realm.type == "realm"
                                    COLLECT realm_item = realm INTO groups = item
                                        RETURN MERGE(realm_item, {users_include_roles: groups})
                            """
        aql = aql.replace("#rolesConditions", rolesConditions)
        queryResult = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result
        return {"items": [self._realmIncludesUsersIncludeRolesByResultItem(x) for x in result], "totalItemCount": len(result)}

    @debugLogger
    def usersIncludeRealmsAndRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                    LET users_include_roles = (FOR user IN resource
                                            FILTER user.type == "user"
                                            FOR role_item IN OUTBOUND user `has`
                                            FILTER role_item.type == "role"
                                            COLLECT user_item = user into groups = role_item
                                                RETURN MERGE(user_item, {roles: groups}))
                    FOR item IN users_include_roles
                        FOR role2 IN item.roles
                            FOR realm IN outbound role2 `access`
                                FILTER realm.type == "realm"
                                COLLECT user_item = item INTO groups = realm
                                    RETURN MERGE(user_item, {realms: groups})
                            """
            queryResult = self._db.AQLQuery(aql, rawResults=True)
            result = queryResult.result
            return {"items": [self._userIncludesRealmsAndRolesByResultItem(x) for x in result],
                    "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                            LET res1 =UNIQUE(FLATTEN(
                                        FOR role IN resource
                                            FILTER (#rolesConditions)
                                            LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == 'realm'
                                                        FOR v2 IN INBOUND v1._id `access` FILTER v2.type == "role" RETURN v2)
                                            LET accesses = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm"
                                                                FOR v2 IN 1..100 OUTBOUND v1._id `has` FILTER v2.type == "realm"
                                                                    FOR v3 IN INBOUND v2._id `access` FILTER v3.type == "role"
                                                                                RETURN v3
                                                                       )
                                            LET roles = UNION_DISTINCT(accesses, direct_access)
                                            RETURN roles
                                        ))

                            LET users_with_roles = (
                                FOR user IN resource
                                    FILTER user.type == "user"
                                    FOR role2 IN res1
                                        FILTER role2.type == "role"
                                        FOR role3 IN OUTBOUND user `has`
                                        FILTER role3.id == role2.id
                                        FOR role4 IN OUTBOUND user `has`
                                            FILTER role4.type == "role"
                                            COLLECT user_item = user into groups = role4
                                                RETURN MERGE(user_item, {roles: unique(groups)}))

                    FOR item IN users_with_roles
                        FOR role2 IN item.roles
                            FOR realm IN outbound role2 `access`
                                FILTER realm.type == "realm"
                                COLLECT user_item = item INTO groups = realm
                                    RETURN MERGE(user_item, {realms: groups})
                                """
        aql = aql.replace("#rolesConditions", rolesConditions)
        queryResult = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result
        return {"items": [self._userIncludesRealmsAndRolesByResultItem(x) for x in result],
                "totalItemCount": len(result)}

    @debugLogger
    def projectsIncludeRealmsIncludeUsersIncludeRoles(
            self,
            tokenData: TokenData = None,
    ) -> dict:
        if TokenService.isSuperAdmin(tokenData=tokenData) or TokenService.isSysAdmin(tokenData=tokenData):
            aql = """
                                LET users_include_roles = (FOR user IN resource
                                                        FILTER user.type == "user"
                                                        FOR role_item IN OUTBOUND user `has`
                                                        FILTER role_item.type == "role"
                                                        COLLECT user_item = user into groups = role_item
                                                            RETURN MERGE(user_item, {roles: groups}))
                                
                                for project in resource
                                    // Filter only project type
                                    filter project.type == "project"
                                    // Loop through all the user items that have roles as a key
                                    for user_item in users_include_roles
                                        for user_item_role in user_item.roles
                                            // User item has connection to a project
                                            for v_project in outbound user_item_role `access`
                                                // Make sure the the user has connection with the same project that we are looping from above
                                                filter v_project.id == project.id
                                                // User item has a connection to a realm
                                                for v_realm in outbound user_item_role `access`
                                                    // Filter only the realm type
                                                    filter v_realm.type == "realm"
                                                    // Group by project and put realm and user into the groups to be processed later
                                                    COLLECT project_item = project into realm_and_user_grp = {realm: v_realm, user_item}
                                                        // Group by realm
                                                        let realm_coll = (for item in realm_and_user_grp
                                                            collect c_realm = item.realm into grp = {user_item: item.user_item, project: project_item}
                                                                return merge(c_realm, {users_include_roles: grp[*].user_item})
                                                                )
                                                        return merge(project_item, {realms_include_users_include_roles: realm_coll})
                            """
            queryResult = self._db.AQLQuery(aql, rawResults=True)
            result = queryResult.result
            return {"items": [self._projectIncludesRealmsIncludeUsersIncludeRolesByResultItem(x) for x in result],
                    "totalItemCount": len(result)}

        rolesConditions = ""
        for role in tokenData.roles():
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                    LET resource_user_id = "#userId" 
                    LET roles =UNIQUE(FLATTEN(
                        FOR role IN resource
                            FILTER (#rolesConditions)
                            LET direct_access = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == 'realm'
                                        FOR v2 IN INBOUND v1._id `access` FILTER v2.type == "role" RETURN v2)
                            LET accesses = (FOR v1 IN OUTBOUND role._id `access` FILTER v1.type == "realm"
                                                FOR v2 IN 1..100 OUTBOUND v1._id `has` FILTER v2.type == "realm"
                                                    FOR v3 IN INBOUND v2._id `access` FILTER v3.type == "role"
                                                                RETURN v3
                                                       )
                            LET roles = UNION_DISTINCT(accesses, direct_access)
                            RETURN roles
                        ))
                    
                    LET users_include_roles = (
                        FOR user IN resource
                            FILTER user.type == "user"
                            FOR role2 IN roles
                                FILTER role2.type == "role"
                                FOR role3 IN OUTBOUND user `has`
                                FILTER role3.id == role2.id
                                FOR role4 IN OUTBOUND user `has`
                                    FILTER role4.type == "role"
                                    COLLECT user_item = user into groups = role4
                                        RETURN merge(user_item, {roles: unique(groups)}))
                    
                    for project in resource
                        // Filter only project type
                        filter project.type == "project"
                        // Loop through all the user items that have roles as a key
                        for user_item in users_include_roles
                            for user_item_role in user_item.roles
                                // User item has connection to a project
                                let prj1 = (for v_project in outbound user_item_role `access` filter v_project.id == project.id return v_project)
                                let prj2 = (for v_project in inbound resource_user_id `owned_by` filter v_project.id == project.id return v_project)
                    
                                filter prj1 != [] or prj2 != []
                                
                                let prj_merged = unique([merge(prj1 != [] ? prj1[0] : {}, prj2 != [] ? prj2[0] : {})])
                                for v_project in prj_merged
                                    // Make sure the the user has connection with the same project that we are looping from above
                                    filter v_project.id == project.id
                                    
                                    // User item has a connection to a realm
                                    for v_realm in outbound user_item_role `access`
                                        // Filter only the realm type
                                        filter v_realm.type == "realm"
                    
                                        // Group by project and put realm and user into the groups to be processed later
                                        COLLECT project_item = project into realm_and_user_grp = {realm: v_realm, user_item}
                                            // Group by realm
                                            let realm_coll = (for item in realm_and_user_grp
                                                collect c_realm = item.realm into grp = {user_item: item.user_item, project: project_item}
                                                    return merge(c_realm, {users_include_roles: grp[*].user_item})
                                                    )
                                            return merge(project_item, {realms_include_users_include_roles: realm_coll})
                                """
        aql = aql.replace("#rolesConditions", rolesConditions)
        aql = aql.replace("#userId", f'resource/{tokenData.id()}')
        queryResult = self._db.AQLQuery(aql, rawResults=True)
        result = queryResult.result
        return {"items": [self._projectIncludesRealmsIncludeUsersIncludeRolesByResultItem(x) for x in result],
                "totalItemCount": len(result)}

    def _projectIncludesRealmsIncludeUsersIncludeRolesByResultItem(self, resultItem):
        return ProjectIncludesRealmsIncludeUsersIncludeRoles.createFrom(
                project=Project.createFrom(id=resultItem["id"], name=resultItem["name"], skipValidation=True),
                realmsIncludeUsersIncludeRoles=[self._realmIncludesUsersIncludeRolesByResultItem(x) for x in resultItem["realms_include_users_include_roles"]]
        )

    def _realmIncludesUsersIncludeRolesByResultItem(self, resultItem):
        return RealmIncludesUsersIncludeRoles.createFrom(
                realm=Realm.createFrom(id=resultItem["id"], name=resultItem["name"], realmType=resultItem["realm_type"]),
                usersIncludeRoles=[self._userIncludesRolesByResultItem(x) for x in resultItem["users_include_roles"]]
        )

    def _userIncludesRealmsAndRolesByResultItem(self, resultItem):
        return UserIncludesRealmsAndRoles.createFrom(
                user=User.createFrom(id=resultItem["id"], email=resultItem["email"]),
                roles=[Role.createFrom(id=role["id"], type=role["type"], name=role["name"], title=role["title"],
                                   skipValidation=True) for role in resultItem["roles"]],
                realms = [Realm.createFrom(id=realm["id"], name=realm["name"], realmType=realm["realm_type"],skipValidation=True)
                          for realm in resultItem["realms"]])

    def _userIncludesRolesByResultItem(self, resultItem):
        return UserIncludesRoles.createFrom(
                user=User.createFrom(id=resultItem["id"], email=resultItem["email"], skipValidation=True),
                roles=[Role.createFrom(id=role["id"], type=role["type"], name=role["name"], title=role["title"],
                                       skipValidation=True) for role in resultItem["roles"]])
    # endregion
























    @debugLogger
    def _filterRoleAccessPermissionDataItems(
        self, roleAccessPermissionDataList: List[RoleAccessPermissionData]
    ) -> List[RoleAccessPermissionData]:
        deniedItems = {"deniedResources": {}, "deniedResourceTypes": {}}
        # Collect denied items
        for roleAccessPermissionData in roleAccessPermissionDataList:
            populatedDeniedItems = self._populateDeniedItems(
                roleAccessPermissionData.permissions
            )
            deniedItems = {**deniedItems, **populatedDeniedItems}
        # Filter items
        for roleAccessPermissionData in roleAccessPermissionDataList:
            filteredAccessTree = self._filterAccessTree(
                roleAccessPermissionData.accessTree, deniedItems
            )
            roleAccessPermissionData.accessTree = filteredAccessTree

        return roleAccessPermissionDataList

    def _filterAccessTree(self, accessTree: List[AccessNode], deniedItems: dict):
        result = []
        for node in accessTree:
            nodeContentType = node.data.contentType
            if nodeContentType is AccessNodeContentTypeConstant.RESOURCE_INSTANCE:
                nodeDataContent: ResourceInstanceAccessNodeContent = (
                    ResourceInstanceAccessNodeContent.castFrom(node.data.content)
                )
                resource = nodeDataContent.resource
                if (
                    resource.id() not in deniedItems["deniedResources"]
                    and resource.type() != PermissionContextConstant.RESOURCE_TYPE
                ):
                    filteredChildren = self._filterAccessTree(
                        node.children, deniedItems
                    )
                    node.children = filteredChildren
                    result.append(node)
        return result

    @debugLogger
    def _populateDeniedItems(
        self, permissionsWithContexts: List[PermissionWithPermissionContexts]
    ):
        deniedItems = {"deniedResources": {}, "deniedResourceTypes": {}}
        for permissionWithContexts in permissionsWithContexts:
            permission = permissionWithContexts.permission
            permissionContexts = permissionWithContexts.permissionContexts
            if PermissionAction.READ in permission.deniedActions():
                for permissionContext in permissionContexts:
                    if (
                        permissionContext.type()
                        == PermissionContextConstant.RESOURCE_TYPE
                    ):
                        data = permissionContext.data()
                        if "name" in data and "deniedResourceTypes" in deniedItems:
                            deniedItems["deniedResourceTypes"][data["name"]] = True
                    if (
                        permissionContext.type()
                        == PermissionContextConstant.RESOURCE_INSTANCE
                    ):
                        data = permissionContext.data()
                        if "id" in data and "deniedResources" in deniedItems:
                            deniedItems["deniedResources"][data["id"]] = True
        return deniedItems

    @debugLogger
    def _filterItems(
        self,
        items,
        roleAccessPermissionDataList: List[RoleAccessPermissionData],
        resourceType: str = "",
    ):
        deniedItems = {"deniedResources": {}, "denyAll": False}
        filteredItems = items
        for roleAccessPermissionData in roleAccessPermissionDataList:
            for permissionWithContexts in roleAccessPermissionData.permissions:
                deniedResult = self._populateDeniedResourcesForRead(
                    permissionWithContexts, resourceType
                )
                if deniedResult["denyAll"]:
                    return []
                # Merge the result
                deniedItems = {**deniedItems, **deniedResult}
                if (
                    PermissionAction.READ
                    in permissionWithContexts.permission.allowedActions()
                ):
                    # Check if it has any resource type that matches the one in the parameter
                    for context in permissionWithContexts.permissionContexts:
                        if context.type() == PermissionContextConstant.RESOURCE_TYPE:
                            contextData = context.data()
                            if "name" in contextData:
                                if contextData["name"] == resourceType:
                                    # We found READ allowed action for the resource type
                                    newItems = (
                                        self._filterOutItemsForResourceTypeByAccessTree(
                                            filteredItems,
                                            roleAccessPermissionData.accessTree,
                                            resourceType,
                                            deniedItems,
                                        )
                                    )
                                    filteredItems.extend(
                                        x for x in newItems if x not in filteredItems
                                    )
        return filteredItems

    def _filterOutItemsForResourceTypeByAccessTree(
        self,
        filteredItems: List[dict],
        accessTree: List[AccessNode],
        resourceType: str,
        deniedItems: dict,
    ):
        result = []
        for node in accessTree:
            # todo to be modified
            nodeContentType = node.data.contentType
            if nodeContentType is AccessNodeContentTypeConstant.RESOURCE_INSTANCE:
                nodeDataContent: ResourceInstanceAccessNodeContent = (
                    ResourceInstanceAccessNodeContent.castFrom(node.data.content)
                )
                resource = nodeDataContent.resource
                if resource.type() == resourceType:
                    if resource.id() not in deniedItems["deniedResources"]:
                        item = self._itemFromFilteredItemsById(
                            filteredItems, resource.id()
                        )
                        if item is not None:
                            result.append(item)
                    # Stop parsing new resources
                    return result
            if len(node.children) > 0:
                newResult = self._filterOutItemsForResourceTypeByAccessTree(
                    filteredItems, node.children, resourceType, deniedItems
                )
                result.extend(x for x in newResult if x not in result)

        return result

    @debugLogger
    def _itemFromFilteredItemsById(self, filteredItems, id):
        for item in filteredItems:
            if item["id"] == id:
                return item
        return None

    @debugLogger
    def _populateDeniedResourcesForRead(self, permissionWithContexts, resourceType):
        result = {"deniedResources": {}, "denyAll": False}
        deniedActions = permissionWithContexts.permission.deniedActions()
        if deniedActions is not [] and PermissionAction.READ in deniedActions:
            for context in permissionWithContexts.permissionContexts:
                contextData = context.data()
                # If the context of type resource_type and the name in the data is the same as of resourceType
                # (ex. ou, realm), then deny all
                if (
                    context.type() == PermissionContextConstant.RESOURCE_TYPE
                    and "name" in contextData
                    and resourceType == contextData["name"]
                ):
                    result["denyAll"] = True
                    break
                elif (
                    context.type() == PermissionContextConstant.RESOURCE_INSTANCE
                    and "id" in contextData
                ):
                    result["deniedResources"][contextData["id"]] = True
        return result

    @debugLogger
    def connectResourceToOwner(self, resource: Resource, tokenData: TokenData):
        userDocId = self.userDocumentId(
            User.createFrom(id=tokenData.id(), email=tokenData.email())
        )
        resourceDocId = self.resourceDocumentId(resource)

        aql = """
            UPSERT {_from: @fromId, _to: @toId}
                INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
              IN owned_by                  
            """
        bindVars = {
            "fromId": resourceDocId,
            "toId": userDocId,
            "fromType": resource.type(),
            "toType": PermissionContextConstant.USER.value,
        }
        _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        for role in tokenData.roles():
            roleDocId = self.roleDocumentId(
                Role.createFrom(id=role["id"], name=role["name"], title=role["title"])
            )
            aql = """
                UPSERT {_from: @fromId, _to: @toId}
                    INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                    UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                  IN owned_by                  
                """
            bindVars = {
                "fromId": resourceDocId,
                "toId": roleDocId,
                "fromType": resource.type(),
                "toType": PermissionContextConstant.ROLE.value,
            }
            _ = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

    @debugLogger
    def roleAccessPermissionsData(
        self, tokenData: TokenData, includeAccessTree: bool = True
    ) -> List[RoleAccessPermissionData]:
        items = self._rawRoleTreeItems(tokenData.roles(), includeAccessTree)
        return self._constructRoleAccessPermissionDataFromRawRoleTreeItems(items)

    @debugLogger
    def _constructRoleAccessPermissionDataFromRawRoleTreeItems(
        self, items
    ) -> List[RoleAccessPermissionData]:
        result = []
        for item in items:
            role = Role.createFrom(**item["role"])
            permissions = item["role"]["_permissions"]
            permList = []
            # For each permission
            for permItem in permissions:
                perm = Permission(
                    id=permItem["permission"]["id"],
                    name=permItem["permission"]["name"],
                    allowedActions=permItem["permission"]["allowed_actions"],
                )
                resList = []
                # Get the permission contexts for the permission
                for resItem in permItem["permission_contexts"]:
                    resList.append(
                        PermissionContext(
                            id=resItem["id"], type=resItem["type"], data=resItem["data"]
                        )
                    )

                p = PermissionWithPermissionContexts(
                    permission=perm, permissionContexts=resList
                )
                # Add it in the permission list
                permList.append(p)
            ownedBy = None
            ownerOf = None
            if item["owned_by"] is not None:
                ownedBy = Resource(
                    id=item["owned_by"]["id"], type=item["owned_by"]["type"]
                )
            if item["owner_of"] is not None:
                ownerOf = []
                for ownerOfItem in item["owner_of"]:
                    if ownerOfItem is not None:
                        ownerOf.append(
                            Resource(id=ownerOfItem["id"], type=ownerOfItem["type"])
                        )
            accessTree = self._fetchAccessTree(accesses=item["accesses"])
            permData = RoleAccessPermissionData(
                role=role,
                permissions=permList,
                ownedBy=ownedBy,
                ownerOf=ownerOf,
                accessTree=accessTree,
            )
            result.append(permData)

        return result

    @debugLogger
    def _rawRoleTreeItems(self, roles: List[dict], includeAccessTree):
        rolesConditions = ""
        for role in roles:
            if rolesConditions == "":
                rolesConditions += f'role.id == "{role["id"]}"'
            else:
                rolesConditions += f' OR role.id == "{role["id"]}"'

        if rolesConditions == "":
            rolesConditions = 'role.id == "None"'
        aql = """
                FOR role IN resource
                    FILTER (#rolesConditions) AND role.type == 'role'
                    LET owned_by = FIRST(FOR v1, e1 IN OUTBOUND role._id `owned_by`
                                        RETURN {"id": v1.id, "name": v1.name, "type": v1.type})
                    LET owner_of = (FOR v1 IN 1..100 INBOUND role._id `owned_by` RETURN v1)
                    LET permissions = (FOR v1, e1 IN OUTBOUND role._id `has`
                                        FILTER e1._from_type == 'role' AND e1._to_type == 'permission'
                                        LET permission_contexts = (FOR v2, e2 IN OUTBOUND v1._id `for`
                                            RETURN {
                                            "id": v2.id,
                                            "type": v2.type,
                                            "data": v2.data})
                                        RETURN {"permission": {"id": v1.id, "name": v1.name, "allowed_actions": v1.allowed_actions}, "permission_contexts": permission_contexts})
                    """
        if includeAccessTree:
            accessTree = """
                LET direct_access = (FOR v1, e1, p IN OUTBOUND role._id `access` RETURN p)
                LET accesses = (FOR v1, e1 IN OUTBOUND role._id `access`
                                    FOR v2, e2, p IN 1..100 OUTBOUND v1._id `has`
                                        RETURN p
                               )
                LET result = UNION_DISTINCT(direct_access, accesses)
                RETURN {"role": {"id": role.id, "name": role.name, "title": role.title, "_permissions": permissions}, "owned_by": owned_by, "owner_of": owner_of, "accesses": result}
                """
            aql += accessTree
        else:
            noAccessTree = """
                RETURN {"role": {"id": role.id, "name": role.name, "title": role.title, "_permissions": permissions}, "owned_by": owned_by, "owner_of": owner_of, "accesses": []}
            """
            aql += noAccessTree
        aql = aql.replace("#rolesConditions", rolesConditions)

        queryResult = self._db.AQLQuery(aql, rawResults=True)
        qResult = queryResult.result
        if len(qResult) == 0:
            return []
        return qResult

    @debugLogger
    def isOwnerOfResource(self, resource: Resource, tokenData: TokenData) -> bool:
        # (v1.id == @ownerId OR v1.id == @ownerId)
        ownerIdConditions = ""
        for role in tokenData.roles():
            if ownerIdConditions == "":
                ownerIdConditions += f'v1.id == "{role["id"]}"'
            else:
                ownerIdConditions += f' OR v1.id == "{role["id"]}"'
        aql = """
            FOR d IN resource
                FILTER d.id == @id
                FOR v1 IN OUTBOUND d._id `owned_by`
                    FILTER (#ownerIdConditions)
                    RETURN 1
            """
        aql = aql.replace("#ownerIdConditions", ownerIdConditions)

        bindVars = {"id": resource.id()}
        queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        qResult = queryResult.result
        if len(qResult) == 0:
            return False
        return True

    @debugLogger
    def _fetchAccessTree(self, accesses: List[dict] = None) -> List[AccessNode]:
        if accesses is None:
            return []

        childrenKeys: Dict[str, bool] = defaultdict()
        objects: Dict[str, AccessNode] = defaultdict()
        result = []

        for acc in accesses:
            for edge in acc["edges"]:
                if edge["_from"] not in objects:
                    self._addAccessKey(
                        result=objects, key=edge["_from"], verts=acc["vertices"]
                    )
                if edge["_to"] not in objects:
                    self._addAccessKey(
                        result=objects, key=edge["_to"], verts=acc["vertices"]
                    )

                found = False
                for child in objects[edge["_from"]].children:
                    resourceInstanceAccessNodeContent: ResourceInstanceAccessNodeContent = ResourceInstanceAccessNodeContent.castFrom(
                        child.data.content
                    )
                    resource = resourceInstanceAccessNodeContent.resource
                    edgeToResource = self._resourceFromAccessNode(objects[edge["_to"]])
                    if resource.id() == edgeToResource.id():
                        found = True
                if not found:
                    childrenKeys[edge["_to"]] = True
                    objects[edge["_from"]].children.append(objects[edge["_to"]])
        for key in objects:
            if key not in childrenKeys:
                result.append(objects[key])
        return result

    def _resourceFromAccessNode(self, accessNode: AccessNode):
        content = accessNode.data.content
        contentType = accessNode.data.contentType
        if contentType is not AccessNodeContentTypeConstant.RESOURCE_INSTANCE:
            raise InvalidResourceException(
                message=f"{PolicyRepositoryImpl._resourceFromAccessNode.__qualname__} invalid resource content: {content}, contentType: {contentType}, accessNode: {accessNode.toMap()}"
            )
        resourceInstanceAccessNodeContent: ResourceInstanceAccessNodeContent = (
            ResourceInstanceAccessNodeContent.castFrom(content)
        )
        return resourceInstanceAccessNodeContent.resource

    def _addAccessKey(self, result: dict, key: str, verts: List[dict]):
        for vert in verts:
            if vert is not None and vert["_id"] == key and "name" in vert:
                node = AccessNode()
                resource = Resource(id=vert["id"], type=vert["type"])
                resourceName = vert["name"]
                node.data.content = ResourceInstanceAccessNodeContent(
                    resource=resource, resourceName=resourceName
                )
                node.data.contentType = AccessNodeContentTypeConstant.RESOURCE_INSTANCE
                node.data.context["resource_type"] = resource.type()
                # Add the node based on the key as '_id'
                result[key] = node
