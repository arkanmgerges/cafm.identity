"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.policy.access_node_content.AccessNodeContent import (
    AccessNodeContent,
    AccessNodeContentTypeConstant,
)


class AccessNodeData:
    def __init__(self):
        self.content: AccessNodeContent = AccessNodeContent(
            dataType=AccessNodeContentTypeConstant.RESOURCE_INSTANCE
        )
        self.contentType: AccessNodeContentTypeConstant = (
            AccessNodeContentTypeConstant.RESOURCE_INSTANCE
        )
        self.context: dict = {}

    def toMap(self):
        return {
            "content": self.content.toMap(),
            "content_type": self.contentType.value,
            "context": self.context,
        }

    def __repr__(self):
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"

    def __str__(self) -> str:
        return f"<{self.__module__} object at {hex(id(self))}> {self.toMap()}"
