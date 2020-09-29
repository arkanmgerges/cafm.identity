"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from pydantic import BaseModel


class Token(BaseModel):
    """
    Using snake case here to be compatible with oauth2 specification
    """
    access_token: str
    token_type: str