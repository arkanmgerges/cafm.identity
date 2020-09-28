"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domainmodel.role.Role import Role


def test_create_role():
    role = Role('1', '2')
    assert isinstance(role, Role)

def test_create_role_with_semantic_constructor():
    id = str(uuid4())
    role = Role.createFrom(id=id, name='Prj1')
    assert isinstance(role, Role)
    assert role.id() == id
    assert role.name() == 'Prj1'
