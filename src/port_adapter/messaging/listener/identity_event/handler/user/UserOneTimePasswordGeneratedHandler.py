"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.user.UserOneTimePasswordGeneratedHandler import (
    UserOneTimePasswordGeneratedHandler as Handler,
)

"""
c4model|cb|identity:ComponentQueue(identity__messaging_identity_event_handler__UserOneTimePasswordGeneratedHandler, "CommonEventConstant.USER_ONE_TIME_PASSWORD_GENERATED.value", "identity event consumer", "")
c4model:Rel(identity__messaging_project_event_handler__UserCreatedHandler, identity__domainmodel_event__UserOneTimePasswordGenerated, "consume")
c4model:Rel(identity__messaging_identity_event_handler__UserOneTimePasswordGeneratedHandler, identity__messaging_identity_command_handler__SendEmailOneTimeUserPasswordHandler, "CommonCommandConstant.SEND_EMAIL_ONE_TIME_USER_PASSWORD.value", "message")
"""


class UserOneTimePasswordGeneratedHandler(Handler):
    pass
