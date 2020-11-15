"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.resource.Resource import Resource


class AccessNode:
    def __init__(self):
        self.resource: Resource
        self.resourceName: str
        self.children: List[AccessNode] = []
