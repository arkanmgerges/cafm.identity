"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from pydantic import BaseModel

class OrganizationalUnit(BaseModel):
    id: str
    name: str
    description: str
