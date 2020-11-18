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

    def toMap(self):
        result = self.resource.toMap()
        result['name'] = self.resourceName
        mapsOfChildren = []
        for child in self.children:
            mapsOfChildren.append(child.toMap())
        result['children'] = mapsOfChildren
        return result


