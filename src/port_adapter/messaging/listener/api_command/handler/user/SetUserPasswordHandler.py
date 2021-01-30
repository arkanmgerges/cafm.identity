"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.port_adapter.messaging.listener.common.handler.user.SetUserPasswordHandler import \
    SetUserPasswordHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__SetUserPasswordHandler, "CommonCommandConstant.SET_USER_PASSWORD.value", "api command consumer", "")
c4model:Rel(api__identity_user_py__setUserPassword__api_command_topic, identity__messaging_api_command_handler__ResetUserPasswordHandler, "CommonCommandConstant.RESET_USER_PASSWORD.value", "message")
c4model:Rel(identity__messaging_api_command_handler__SetUserPasswordHandler, identity__messaging_api_command_handler__SetUserPasswordHandler, "CommonCommandConstant.SET_USER_PASSWORD.value", "message")
"""


class SetUserPasswordHandler(Handler):
    pass
