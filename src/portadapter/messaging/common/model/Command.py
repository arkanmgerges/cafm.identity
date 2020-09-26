"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from __future__ import annotations

import os
import time
from enum import Enum

from avro_models.core import avro_schema, AvroModelContainer

from src.portadapter.messaging.common.model.MessageBase import MessageBase

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


class COMMANDS(str, Enum):
    CREATE_USER = 'createUser'


@avro_schema(AvroModelContainer(default_namespace="coral.api"),
             schema_file=os.path.join(DIR_NAME, "api-command.avsc"))
class Command(MessageBase):
    def __init__(self, id, creatorServiceName='coral.api', name='', data='', createdOn=round(time.time())):
        super().__init__({'id': id, 'creatorServiceName': creatorServiceName, 'name': name, 'createdOn': createdOn, 'data': data})

    def toMap(self, thisObjectForMapping=None, _ctx=None):
        return vars(self)['_value']

    def topic(self):
        return os.getenv('CORAL_API_COMMAND_TOPIC', None)