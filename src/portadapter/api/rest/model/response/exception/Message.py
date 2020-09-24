"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from pydantic import BaseModel


class MessageDetail(BaseModel):
    msg: str


class Message(BaseModel):
    detail: List[MessageDetail]
