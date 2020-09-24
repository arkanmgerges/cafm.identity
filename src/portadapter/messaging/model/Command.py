from __future__ import annotations

import os
import time
from enum import Enum

from avro_models.core import avro_schema, AvroModelContainer

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../avro'


class COMMANDS(str, Enum):
    CREATE_USER = 'createUser'


@avro_schema(AvroModelContainer(default_namespace="coral.api"),
             schema_file=os.path.join(DIR_NAME, "api-command.avsc"))
class Command(object):
    def __init__(self, id, creatorServiceName='coral.api', name=None, createdOn=round(time.time())):
        super().__init__({'id': id, 'creatorServiceName': creatorServiceName, 'name': name, 'createdOn': createdOn})

    def toMap(self, _ctx=None):
        return vars(self)['_value']
