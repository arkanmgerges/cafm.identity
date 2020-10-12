"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.ou.Ou import Ou


def test_create_ou():
    # Act
    ou = Ou('1', '2')
    # Assert
    assert isinstance(ou, Ou)


def test_create_ou_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    ou = Ou.createFrom(id=id, name='Prj1')
    # Assert
    assert isinstance(ou, Ou)
    assert ou.id() == id
    assert ou.name() == 'Prj1'
