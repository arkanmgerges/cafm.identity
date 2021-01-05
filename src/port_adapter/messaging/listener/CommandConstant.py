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
    CREATE_RESOURCE_TYPE = 'create_permission_context'
    DELETE_RESOURCE_TYPE = 'delete_permission_context'
    UPDATE_RESOURCE_TYPE = 'update_permission_context'
    CREATE_USER_GROUP = 'create_user_group'
    DELETE_USER_GROUP = 'delete_user_group'
    UPDATE_USER_GROUP = 'update_user_group'
    ASSIGN_ROLE_TO_USER = 'assign_role_to_user'
    REVOKE_ASSIGNMENT_ROLE_TO_USER = 'revoke_assignment_role_to_user'
    ASSIGN_ROLE_TO_USER_GROUP = 'assign_role_to_user_group'
    REVOKE_ASSIGNMENT_ROLE_TO_USER_GROUP = 'revoke_assignment_role_to_user_group'
    ASSIGN_USER_TO_USER_GROUP = 'assign_user_to_user_group'
    REVOKE_ASSIGNMENT_USER_TO_USER_GROUP = 'revoke_assignment_user_to_user_group'
    ASSIGN_PERMISSION_TO_PERMISSION_CONTEXT = 'assign_permission_to_permission_context'
    REVOKE_ASSIGNMENT_PERMISSION_TO_PERMISSION_CONTEXT = 'revoke_assignment_permission_to_permission_context'
    ASSIGN_ROLE_TO_PERMISSION = 'assign_role_to_permission'
    REVOKE_ASSIGNMENT_ROLE_TO_PERMISSION = 'revoke_assignment_role_to_permission'
    GRANT_ACCESS_ROLE_TO_RESOURCE = 'grant_access_role_to_resource'
    REVOKE_ACCESS_ROLE_TO_RESOURCE = 'revoke_access_role_to_resource'
    ASSIGN_RESOURCE_TO_RESOURCE = 'assign_resource_to_resource'
    REVOKE_ASSIGNMENT_RESOURCE_TO_RESOURCE = 'revoke_assignment_resource_to_resource'
    SEND_EMAIL_ONE_TIME_USER_PASSWORD = 'send_email_one_time_user_password'
    GENERATE_USER_ONE_TIME_PASSWORD = 'generate_user_one_time_password'
    DELETE_USER_ONE_TIME_PASSWORD = 'delete_user_one_time_password'

@extendEnum(CommonCommandConstant)
class ApiCommandConstant(Enum):
    pass


@extendEnum(CommonCommandConstant)
class IdentityCommandConstant(Enum):
    pass
