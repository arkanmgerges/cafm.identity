"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from mock import Mock

from src.domain_model.authorization.AuthorizationRepository import AuthorizationRepository
from src.domain_model.authorization.AuthorizationService import AuthorizationService
from src.domain_model.policy.PolicyControllerService import PolicyControllerService


def test_hash_keys():
    # Arrange
    authz = AuthorizationService(authzRepo=Mock(spec=AuthorizationRepository), policyService=Mock(spec=PolicyControllerService))
    data = [
        {'key': 'GET:/v1/project/projects/{project_id}/buildings/{building_id}/building_levels/{building_level_id}/building_level_rooms/{building_level_room_id}'},
        {'key': 'PUT:/v1/project/projects/{project_id}/buildings/{building_id}/building_levels/{building_level_id}/building_level_rooms/{building_level_room_id}/update_index'},
        {'key': 'PUT:/v1/project/users/{user_id}'},
    ]
    # Act
    result = authz.hashKeys(keys=data)
    # Assert
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]['key'] == 'GET:/v1/project/projects/{project_id}/buildings/{building_id}/building_levels/{building_level_id}/building_level_rooms/{building_level_room_id}'
    assert len(result[0]['hashCode']) > 0
