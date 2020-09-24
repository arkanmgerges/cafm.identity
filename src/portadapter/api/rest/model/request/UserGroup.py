"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class UserGroup(BaseModel):
    id: str
    name: str

