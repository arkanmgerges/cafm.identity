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


class CommonEventConstant(Enum):
    OU_CREATED = "ou_created"
    OU_DELETED = "ou_deleted"
    OU_UPDATED = "ou_updated"
    PERMISSION_CREATED = "permission_created"
    PERMISSION_DELETED = "permission_deleted"
    PERMISSION_UPDATED = "permission_updated"
    PERMISSION_CONTEXT_CREATED = "permission_context_created"
    PERMISSION_CONTEXT_DELETED = "permission_context_deleted"
    PERMISSION_CONTEXT_UPDATED = "permission_context_updated"
    PROJECT_CREATED = "project_created"
    PROJECT_DELETED = "project_deleted"
    PROJECT_UPDATED = "project_updated"
    REALM_CREATED = "realm_created"
    REALM_DELETED = "realm_deleted"
    REALM_UPDATED = "realm_updated"
    ROLE_CREATED = "role_created"
    ROLE_DELETED = "role_deleted"
    ROLE_UPDATED = "role_updated"
    USER_CREATED = "user_created"
    USER_ONE_TIME_PASSWORD_GENERATED = "user_one_time_password_generated"
    USER_WITH_ONE_TIME_PASSWORD_LOGGED_IN = "user_with_one_time_password_logged_in"
    USER_DELETED = "user_deleted"
    USER_UPDATED = "user_updated"
    USER_GROUP_CREATED = "user_group_created"
    USER_GROUP_DELETED = "user_group_deleted"
    USER_GROUP_UPDATED = "user_group_updated"
    USER_PASSWORD_SET = "user_password_set"
    ROLE_TO_USER_ASSIGNED = "role_to_user_assigned"
    ROLE_TO_USER_GROUP_ASSIGNED = "role_to_user_group_assigned"
    USER_TO_USER_GROUP_ASSIGNED = "user_to_user_group_assigned"
    USER_TO_USER_GROUP_ASSIGNMENT_REVOKED = "user_to_user_group_assignment_revoked"
    ROLE_TO_USER_GROUP_REVOKED = "role_to_user_group_revoked"
    ROLE_TO_USER_ASSIGNMENT_REVOKED = "role_to_user_assignment_revoked"
    USER_TO_REALM_ASSIGNED = "user_to_realm_assigned"
    ROLE_TO_PERMISSION_ASSIGNED = "role_to_permission_assigned"
    ROLE_TO_RESOURCE_ACCESS_GRANTED = "role_to_resource_access_granted"
    ROLE_TO_RESOURCE_ACCESS_REVOKED = "role_to_resource_access_revoked"
    ROLE_TO_PERMISSION_ASSIGNMENT_REVOKED = "role_to_permission_assignment_revoked"
    RESOURCE_TO_RESOURCE_ASSIGNED = "resource_to_resource_assigned"
    RESOURCE_TO_RESOURCE_ASSIGNMENT_REVOKED = "resource_to_resource_assignment_revoked"
    USER_TO_REALM_ASSIGNMENT_REVOKED = "user_to_realm_assignment_revoked"
    PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNED = (
        "permission_to_permission_context_assigned"
    )
    PERMISSION_TO_PERMISSION_CONTEXT_ASSIGNMENT_REVOKED = (
        "permission_to_permission_context_assignment_revoked"
    )
    ORGANIZATION_UPDATED = "organization_updated"
    ROLE_TO_REALM_ASSIGNED = "role_to_realm_assigned"
    ROLE_TO_REALM_ASSIGNMENT_REVOKED = "role_to_realm_assignment_revoked"
    ROLE_TO_PROJECT_ASSIGNED = "role_to_project_assigned"
    ROLE_TO_PROJECT_ASSIGNMENT_REVOKED = "role_to_project_assignment_revoked"
