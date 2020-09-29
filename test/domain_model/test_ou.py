"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.ou.Ou import Ou


def test_create_ou():
    ou = Ou('1', '2')
    assert isinstance(ou, Ou)

def test_create_ou_with_semantic_constructor():
    id = str(uuid4())
    ou = Ou.createFrom(id=id, name='Prj1')
    assert isinstance(ou, Ou)
    assert ou.id() == id
    assert ou.name() == 'Prj1'
