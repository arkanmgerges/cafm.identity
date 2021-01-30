"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.role.DeleteRoleHandler import DeleteRoleHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteRoleHandler, "CommonCommandConstant.DELETE_ROLE.value", "api command consumer", "")
c4model:Rel(api__identity_role_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteRoleHandler, "CommonCommandConstant.DELETE_ROLE.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteRoleHandler, identity__domainmodel_event__RoleDeleted, "create")
"""


class DeleteRoleHandler(Handler):
    pass
