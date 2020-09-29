"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time

from avro_models.core import avro_schema, AvroModelContainer

from src.port_adapter.messaging.common.model.MessageBase import MessageBase

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


@avro_schema(AvroModelContainer(default_namespace="coral.identity"),
             schema_file=os.path.join(DIR_NAME, "identity-event.avsc"))
class IdentityEvent(MessageBase):
    def __init__(self, id, creatorServiceName='coral.identity', name='', data='', occurredOn=round(time.time() * 1000)):
        super().__init__(
            {'id': id, 'creatorServiceName': creatorServiceName, 'name': name, 'occurredOn': occurredOn, 'data': data})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CORAL_IDENTITY_EVENT_TOPIC', 'coral.identity.evt')

    def msgId(self):
        return self.id
