"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.user.UserWithOneTimePasswordLoggedInHandler import \
    UserWithOneTimePasswordLoggedInHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_identity_event_handler__UserWithOneTimePasswordLoggedInHandler, "CommonEventConstant.USER_WITH_ONE_TIME_PASSWORD_LOGGED_IN.value", "identity event consumer", "")
c4model:Rel(identity__messaging_identity_event_handler__UserWithOneTimePasswordLoggedInHandler, identity__messaging_identity_command_handler__DeleteUserOneTimePasswordHandler, "CommonCommandConstant.DELETE_USER_ONE_TIME_PASSWORD.value", "message")
c4model:Rel(identity__messaging_identity_event_handler__UserWithOneTimePasswordLoggedInHandler, identity__domainmodel_event__UserWithOneTimePasswordLoggedIn, "consume")
"""


class UserWithOneTimePasswordLoggedInHandler(Handler):
    pass
