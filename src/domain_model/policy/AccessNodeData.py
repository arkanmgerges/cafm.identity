"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from random import randint

from src.domain_model.policy.access_node_content.AccessNodeContent import AccessNodeContent, \
    AccessNodeContentTypeConstant


class AccessNodeData:
    def __init__(self):
        self.content: AccessNodeContent = AccessNodeContent(dataType=AccessNodeContentTypeConstant.RESOURCE_INSTANCE)
        self.contentType: AccessNodeContentTypeConstant = AccessNodeContentTypeConstant.RESOURCE_INSTANCE
        self.context: dict = {}

    def toMap(self):
        return {"content": self.content.toMap(), "content_type": self.contentType.value, "context": self.context}