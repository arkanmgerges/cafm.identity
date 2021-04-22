"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from uuid import uuid4

from src.domain_model.permission_context.PermissionContext import (
    PermissionContext,
    PermissionContextConstant,
)


def test_create_permissionCotext():
    # Act
    permissionContext = PermissionContext("1")
    # Assert
    assert isinstance(permissionContext, PermissionContext)


def test_create_permissionContext_with_semantic_constructor():
    # Arrange
    id = str(uuid4())
    # Act
    permissionContext = PermissionContext.createFrom(
        id=id, type=PermissionContextConstant.RESOURCE_INSTANCE.value
    )
    # Assert
    assert isinstance(permissionContext, PermissionContext)
    assert permissionContext.type() == PermissionContextConstant.RESOURCE_INSTANCE.value
    assert permissionContext.id() == id


def test_that_two_objects_with_same_attributes_are_equal():
    # Act
    object1 = PermissionContext.createFrom("1234")
    object2 = PermissionContext.createFrom("1234")
    # Assert
    assert object1 == object2


def test_that_two_objects_with_different_attributes_are_not_equal():
    # Act
    object1 = PermissionContext.createFrom(
        "1234", type=PermissionContextConstant.RESOURCE_INSTANCE.value
    )
    object2 = PermissionContext.createFrom(
        "1234", type=PermissionContextConstant.RESOURCE_TYPE.value
    )
    # Assert
    assert object1 != object2


def test_that_inserting_data_and_retrieving_an_item_from_it():
    # Act
    object1 = PermissionContext.createFrom(
        "1234",
        type=PermissionContextConstant.RESOURCE_INSTANCE.value,
        data={"item1": "value1", "item2": {"sub-item2": "value1-2"}},
    )
    # Assert
    assert object1.data()["item1"] == "value1"
    assert object1.data()["item2"]["sub-item2"] == "value1-2"


def test_create_object_without_id_and_verify_that_the_created_object_has_id():
    # Act
    object1 = PermissionContext.createFrom(
        type=PermissionContextConstant.RESOURCE_INSTANCE.value, data={}
    )
    # Assert
    assert object1.id() is not None
    assert object1.id() != ""
    assert isinstance(object1.id(), str)
