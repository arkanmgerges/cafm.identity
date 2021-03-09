"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List, Callable

from src.port_adapter.messaging.listener.common.handler.realm.DeleteRealmHandler import DeleteRealmHandler as Handler

"""
c4model|cb|identity:ComponentQueue(identity__messaging_api_command_handler__DeleteRealmHandler, "CommonCommandConstant.DELETE_REALM.value", "api command consumer", "")
c4model:Rel(api__identity_realm_py__delete__api_command_topic, identity__messaging_api_command_handler__DeleteRealmHandler, "CommonCommandConstant.DELETE_REALM.value", "message")
c4model:Rel(identity__messaging_api_command_handler__DeleteRealmHandler, identity__domainmodel_event__RealmDeleted, "create")
"""


class DeleteRealmHandler(Handler):
    @staticmethod
    def targetsOnException() -> List[Callable]:
        return [Handler.targetOnException]

    @staticmethod
    def targetsOnSuccess() -> List[Callable]:
        return [Handler.targetOnSuccess]