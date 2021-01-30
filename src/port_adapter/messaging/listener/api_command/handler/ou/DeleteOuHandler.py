"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.ou.DeleteOuHandler import DeleteOuHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteOuHandler, "CommonCommandConstant.DELETE_OU.value", "api command consumer", "")
c4model:Rel(api__identity_ou_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteOuHandler, "CommonCommandConstant.DELETE_OU.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteOuHandler, identity__domainmodel_event__OuDeleted, "create")
"""


class DeleteOuHandler(Handler):
    pass
