"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.domain_model.event.EventConstant import CommonEventConstant
from src.port_adapter.messaging.listener.common.handler.user.GenerateUserOneTimePasswordHandler import (
    GenerateUserOneTimePasswordHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_project_event_handler__UserCreatedHandler, "CommonEventConstant.USER_CREATED.value", "project event consumer", "Generate user one time password")
c4model:Rel(identity__messaging_project_event_handler__UserCreatedHandler, identity__domainmodel_event__UserOneTimePasswordGenerated, "create")
c4model:Rel(identity__messaging_project_event_handler__UserCreatedHandler, project__domainmodel_event__UserCreated, "consume")
"""


class UserCreatedHandler(Handler):
    def canHandle(self, name: str) -> bool:
        return name == CommonEventConstant.USER_CREATED.value
