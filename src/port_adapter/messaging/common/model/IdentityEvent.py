"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time

from avro_models.core import avro_schema, AvroModelContainer

from src.port_adapter.messaging.common.model.MessageBase import MessageBase

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


@avro_schema(AvroModelContainer(default_namespace="cafm.identity"),
             schema_file=os.path.join(DIR_NAME, "identity-event.avsc"))
class IdentityEvent(MessageBase):
    def __init__(self, id, creatorServiceName='cafm.identity', name='', metadata='', data='',
                 occurredOn=round(time.time() * 1000), external=None):
        if external is None:
            external = []

        super().__init__(
            {'id': id, 'creator_service_name': creatorServiceName, 'name': name, 'occurred_on': occurredOn,
             'metadata': metadata, 'data': data, 'external': external})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CAFM_IDENTITY_EVENT_TOPIC', 'cafm.identity.evt')

    def msgId(self):
        return self.id
