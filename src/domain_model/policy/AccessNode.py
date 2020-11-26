"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.policy.AccessNodeData import AccessNodeData


class AccessNode:
    def __init__(self):
        self.data: AccessNodeData = AccessNodeData()
        self.children: List[AccessNode] = []

    def toMap(self):
        result = self.data.toMap()
        mapsOfChildren = []
        for child in self.children:
            mapsOfChildren.append(child.toMap())
        result['children'] = mapsOfChildren
        return result
