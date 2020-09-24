"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class TokenData(BaseModel):
    username: str = None