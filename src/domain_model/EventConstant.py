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
    OU_CREATED = 'ou_created'
    OU_DELETED = 'ou_deleted'
    OU_UPDATED = 'ou_updated'
    PERMISSION_CREATED = 'permission_created'
    PERMISSION_DELETED = 'permission_deleted'
    PERMISSION_UPDATED = 'permission_updated'
    PERMISSION_CONTEXT_CREATED = 'permission_context_created'
    PERMISSION_CONTEXT_DELETED = 'permission_context_deleted'
    PERMISSION_CONTEXT_UPDATED = 'permission_context_updated'
    PROJECT_CREATED = 'project_created'
    PROJECT_DELETED = 'project_deleted'
    PROJECT_UPDATED = 'project_updated'
    REALM_CREATED = 'realm_created'
    REALM_DELETED = 'realm_deleted'
    REALM_UPDATED = 'realm_updated'
    ROLE_CREATED = 'role_created'
    ROLE_DELETED = 'role_deleted'
    ROLE_UPDATED = 'role_updated'
    USER_CREATED = 'user_created'
    USER_DELETED = 'user_deleted'
    USER_UPDATED = 'user_updated'
    USER_GROUP_CREATED = 'user_group_created'
    USER_GROUP_DELETED = 'user_group_deleted'
    USER_GROUP_UPDATED = 'user_group_updated'

