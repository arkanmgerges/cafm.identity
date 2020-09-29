"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class Realm(BaseModel):

    id: int
    title: str
    description: str
