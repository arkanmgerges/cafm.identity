"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

import enum


class ConsumerOffsetReset(enum.Enum):
    earliest = 1
    latest = 2
