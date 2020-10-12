"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.permission.Permission import Permission


def test_create_permission():
    # Act
    permission = Permission('1', '2')
    # Assert
    assert isinstance(permission, Permission)


def test_create_permission_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    permission = Permission.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(permission, Permission)
    assert permission.id() == id
    assert permission.name() == 'Prj1'
