"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.permission_context.CreatePermissionContextHandler import \
    CreatePermissionContextHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreatePermissionContextHandler, "CommonCommandConstant.CREATE_RESOURCE_TYPE.value", "api command consumer", "")
c4model:Rel(api__identity_permission_context_py__create__api_command_topic, identity__messaging_api_command_handler__CreatePermissionContextHandler, "CommonCommandConstant.CREATE_RESOURCE_TYPE.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreatePermissionContextHandler, identity__domainmodel_event__PermissionContextCreated, "create")
"""


class CreatePermissionContextHandler(Handler):
    pass
