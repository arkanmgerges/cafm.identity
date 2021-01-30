"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.project.UpdateProjectHandler import \
    UpdateProjectHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateProjectHandler, "CommonCommandConstant.UPDATE_PROJECT.value", "api command consumer", "")
c4model:Rel(api__project_project_py__update__api_command_topic, identity__messaging_api_command_handler__UpdateProjectHandler, "CommonCommandConstant.UPDATE_PROJECT.value", "message")
c4model:Rel(identity__messaging_api_command_handler__UpdateProjectHandler, identity__domainmodel_event__ProjectUpdated, "create")
"""


class UpdateProjectHandler(Handler):
    pass
