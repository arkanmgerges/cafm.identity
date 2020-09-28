"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domainmodel.resourcetype.ResourceType import ResourceType


def test_create_resourceType():
    resourceType = ResourceType('1', '2')
    assert isinstance(resourceType, ResourceType)

def test_create_resourceType_with_semantic_constructor():
    id = str(uuid4())
    resourceType = ResourceType.createFrom(id=id, name='Prj1')
    assert isinstance(resourceType, ResourceType)
    assert resourceType.id() == id
    assert resourceType.name() == 'Prj1'
