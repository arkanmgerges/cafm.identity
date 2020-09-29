"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    description: str
    email: str
    password: str