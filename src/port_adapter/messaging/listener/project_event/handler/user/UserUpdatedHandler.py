"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.user.UpdateUserHandler import (
    UpdateUserHandler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_project_event_handler__UserUpdatedHandler, "CommonEventConstant.USER_UPDATED.value", "project event consumer", "")
c4model:Rel(identity__messaging_project_event_handler__UserUpdatedHandler, identity__domainmodel_event__UserUpdated, "create")
c4model:Rel(identity__messaging_project_event_handler__UserUpdatedHandler, project__domainmodel_event__UserUpdated, "consume")
"""


class UserUpdatedHandler(UpdateUserHandler):
    def targetsOnSuccess(self):
        return []

    def targetsOnException(self):
        return []
