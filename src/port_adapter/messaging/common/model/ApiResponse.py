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


@avro_schema(AvroModelContainer(default_namespace="cafm.api"),
             schema_file=os.path.join(DIR_NAME, "api-response.avsc"))
class ApiResponse(MessageBase):
    def __init__(self, commandId, commandName, metadata='', version=1, data='', creatorServiceName='', success=False,
                 createdOn=None):
        createdOn = DateTimeHelper.utcNow() if createdOn is None else createdOn
        super().__init__(
            {'command_id': commandId, 'command_name': commandName, 'metadata': metadata, 'version': version,
             'data': data, 'creator_service_name': creatorServiceName,
             'success': success, 'created_on': createdOn})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CAFM_API_RESPONSE_TOPIC', 'cafm.api.rsp')

    def msgId(self):
        return self.command_id

    def msgKey(self):
        import json
        dataDict = json.loads(self.data)
        return dataDict['id'] if dataDict is not None and 'id' in dataDict else self.msgId()
