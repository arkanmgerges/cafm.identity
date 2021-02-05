"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.realm.UpdateRealmHandler import UpdateRealmHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__UpdateRealmHandler, "CommonCommandConstant.UPDATE_REALM.value", "api command consumer", "")
c4model:Rel(api__identity_realm_py__update__api_command_topic, identity__messaging_api_command_handler__UpdateRealmHandler, "CommonCommandConstant.UPDATE_REALM.value", "message")
c4model:Rel(identity__messaging_api_command_handler__UpdateRealmHandler, identity__domainmodel_event__RealmUpdated, "create")
"""


class UpdateRealmHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]
