"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domainmodel.realm.Realm import Realm


def test_create_realm():
    realm = Realm('1', '2')
    assert isinstance(realm, Realm)

def test_create_realm_with_semantic_constructor():
    id = str(uuid4())
    realm = Realm.createNew(id=id, name='ComABC')
    assert isinstance(realm, Realm)
    assert realm.id() == id
    assert realm.name() == 'ComABC'
