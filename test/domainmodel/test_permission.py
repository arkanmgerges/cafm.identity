"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domainmodel.permission.Permission import Permission


def test_create_permission():
    permission = Permission('1', '2')
    assert isinstance(permission, Permission)

def test_create_permission_with_semantic_constructor():
    id = str(uuid4())
    permission = Permission.createFrom(id=id, name='Prj1')
    assert isinstance(permission, Permission)
    assert permission.id() == id
    assert permission.name() == 'Prj1'
