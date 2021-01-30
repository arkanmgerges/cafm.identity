"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.permission.CreatePermissionHandler import \
    CreatePermissionHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__CreatePermissionHandler, "CommonCommandConstant.CREATE_PERMISSION.value", "api command consumer", "")
c4model:Rel(api__identity_permission_py__create__api_command_topic, identity__messaging_api_command_handler__CreatePermissionHandler, "CommonCommandConstant.CREATE_PERMISSION.value", "message")
c4model:Rel(identity__messaging_api_command_handler__CreatePermissionHandler, identity__domainmodel_event__PermissionCreated, "create")
"""


class CreatePermissionHandler(Handler):
    pass
