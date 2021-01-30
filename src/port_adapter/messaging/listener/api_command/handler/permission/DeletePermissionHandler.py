"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.permission.DeletePermissionHandler import \
    DeletePermissionHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeletePermissionHandler, "CommonCommandConstant.DELETE_PERMISSION.value", "api command consumer", "")
c4model:Rel(api__identity_permission_py__delete__api_command_topic, identity__messaging_api_command_handler__DeletePermissionHandler, "CommonCommandConstant.DELETE_PERMISSION.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeletePermissionHandler, identity__domainmodel_event__PermissionDeleted, "create")
"""


class DeletePermissionHandler(Handler):
    pass
