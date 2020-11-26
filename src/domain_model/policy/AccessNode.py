"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from typing import List

from src.domain_model.policy.access_node_content.AccessNodeContent import AccessNodeContent, \
    AccessNodeContentTypeConstant


class AccessNodeData:
    content: AccessNodeContent = AccessNodeContent(dataType=AccessNodeContentTypeConstant.RESOURCE_INSTANCE)
    contentType: AccessNodeContentTypeConstant
    context: dict = {}

    def toMap(self):
        return {"content": self.content.toMap(), "content_type": self.contentType.value, "context": self.context}


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
