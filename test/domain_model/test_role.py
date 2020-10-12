"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.role.Role import Role


def test_create_role():
    # Act
    role = Role('1', '2')
    # Assert
    assert isinstance(role, Role)


def test_create_role_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    role = Role.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(role, Role)
    assert role.id() == id
    assert role.name() == 'Prj1'
