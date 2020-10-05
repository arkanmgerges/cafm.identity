"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time

from avro_models.core import avro_schema, AvroModelContainer

from src.port_adapter.messaging.common.model.MessageBase import MessageBase

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


@avro_schema(AvroModelContainer(default_namespace="cafm.api"),
             schema_file=os.path.join(DIR_NAME, "api-command.avsc"))
class ApiCommand(MessageBase):
    def __init__(self, id, creatorServiceName='cafm.api', name='', metadata='', data='',
                 createdOn=round(time.time() * 1000)):
        super().__init__(
            {'id': id, 'creatorServiceName': creatorServiceName, 'name': name, 'createdOn': createdOn,
             'metadata': metadata, 'data': data})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CAFM_API_COMMAND_TOPIC', None)

    def msgId(self):
        return self.id