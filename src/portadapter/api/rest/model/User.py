"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str = None
    fullName: str = None
    disabled: bool = None