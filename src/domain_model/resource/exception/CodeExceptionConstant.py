"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from enum import Enum


class CodeExceptionConstant(Enum):
    OBJECT_EXCEPTION = 100
    OBJECT_ALREADY_EXIST = 101
    OBJECT_DOES_NOT_EXIST = 102
    INVALID_CREDENTIALS = 103
    UN_AUTHORIZED_ACTION = 104
    OBJECT_COULD_NOT_BE_DELETED = 105
    OBJECT_COULD_NOT_BE_UPDATED = 106
    OBJECT_IDENTICAL = 107
