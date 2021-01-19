"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time

from avro_models.core import avro_schema, AvroModelContainer

from src.port_adapter.messaging.common.model.MessageBase import MessageBase
from src.resource.common.DateTimeHelper import DateTimeHelper

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


@avro_schema(AvroModelContainer(default_namespace="cafm.identity"),
             schema_file=os.path.join(DIR_NAME, "identity-command.avsc"))
class IdentityCommand(MessageBase):
    def __init__(self, id, creatorServiceName='cafm.identity', name='', version=1, metadata='', data='',
                 createdOn=None, external=None):
        createdOn = DateTimeHelper.utcNow() if createdOn is None else createdOn
        super().__init__(
            {'id': id, 'creator_service_name': creatorServiceName, 'name': name, 'version': version,
             'created_on': createdOn,'metadata': metadata, 'data': data, 'external': external})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CAFM_IDENTITY_COMMAND_TOPIC', 'cafm.identity.cmd')

    def msgId(self):
        return self.id

    def msgKey(self):
        import json
        dataDict = json.loads(self.data)
        return dataDict['id'] if 'id' in dataDict else self.msgId()
