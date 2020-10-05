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
             schema_file=os.path.join(DIR_NAME, "api-response.avsc"))
class ApiResponse(MessageBase):
    def __init__(self, commandId, commandName, metadata='', data='', creatorServiceName='', success=False,
                 createdOn=round(time.time() * 1000)):
        super().__init__(
            {'commandId': commandId, 'commandName': commandName, 'metadata': metadata, 'data': data,
             'creatorServiceName': creatorServiceName,
             'success': success, 'createdOn': createdOn})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CAFM_API_RESPONSE_TOPIC', 'cafm.api.rsp')

    def msgId(self):
        return self.commandId
