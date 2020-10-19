"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum


def extendEnum(inheritedEnum):
    def wrapper(addedEnum):
        joined = {}
        for item in inheritedEnum:
            joined[item.name] = item.value
        for item in addedEnum:
            joined[item.name] = item.value
        return Enum(addedEnum.__name__, joined)

    return wrapper


class CommonCommandConstant(Enum):
    CREATE_USER = 'create_user'
    DELETE_USER = 'delete_user'
    UPDATE_USER = 'update_user'
    CREATE_ROLE = 'create_role'
    DELETE_ROLE = 'delete_role'
    UPDATE_ROLE = 'update_role'
    CREATE_OU = 'create_ou'
    DELETE_OU = 'delete_ou'
    UPDATE_OU = 'update_ou'
    CREATE_PERMISSION = 'create_permission'
    DELETE_PERMISSION = 'delete_permission'
    UPDATE_PERMISSION = 'update_permission'
    CREATE_PROJECT = 'create_project'
    DELETE_PROJECT = 'delete_project'
    UPDATE_PROJECT = 'update_project'
    CREATE_REALM = 'create_realm'
    DELETE_REALM = 'delete_realm'
    UPDATE_REALM = 'update_realm'
    CREATE_RESOURCE_TYPE = 'create_resource_type'
    DELETE_RESOURCE_TYPE = 'delete_resource_type'
    UPDATE_RESOURCE_TYPE = 'update_resource_type'
    CREATE_USER_GROUP = 'create_user_group'
    DELETE_USER_GROUP = 'delete_user_group'
    UPDATE_USER_GROUP = 'update_user_group'
    ASSIGN_ROLE_TO_USER = 'assign_role_to_user'
    REVOKE_ASSIGNMENT_ROLE_TO_USER = 'revoke_assignment_role_to_user'
    ASSIGN_ROLE_TO_USER_GROUP = 'assign_role_to_user_group'
    REVOKE_ASSIGNMENT_ROLE_TO_USER_GROUP = 'revoke_assignment_role_to_user_group'
    ASSIGN_USER_TO_USER_GROUP = 'assign_user_to_user_group'
    REVOKE_ASSIGNMENT_USER_TO_USER_GROUP = 'revoke_assignment_user_to_user_group'


@extendEnum(CommonCommandConstant)
class ApiCommandConstant(Enum):
    pass


@extendEnum(CommonCommandConstant)
class IdentityCommandConstant(Enum):
    pass
