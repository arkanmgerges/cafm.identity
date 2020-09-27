"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time

from avro_models.core import avro_schema, AvroModelContainer

from src.portadapter.messaging.common.model.MessageBase import MessageBase

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


@avro_schema(AvroModelContainer(default_namespace="coral.identity"),
             schema_file=os.path.join(DIR_NAME, "identity-command.avsc"))
class IdentityCommand(MessageBase):
    def __init__(self, id, serviceName='coral.identity', name='', data='', createdOn=round(time.time() * 1000),
                 externalId=None, externalServiceName=None, externalName=None, externalData=None,
                 externalCreatedOn=None):
        super().__init__(
            {'id': id, 'serviceName': serviceName, 'name': name, 'createdOn': createdOn, 'data': data,
             'externalId': externalId, 'externalServiceName': externalServiceName, 'externalName': externalName,
             'externalCreatedOn': externalCreatedOn, 'externalData': externalData})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CORAL_IDENTITY_COMMAND_TOPIC', None)

    def msgId(self):
        return self.id
