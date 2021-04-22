"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.token.TokenData import TokenData
from src.domain_model.token.TokenService import TokenService


def test_generate_and_validate_token():
    # Arrange
    payload = {
        "id": "1234",
        "email": "user_1@local.test",
        "roles": [{"id": "5678", "name": "admin"}],
    }
    # Act
    token = TokenService.generateToken(payload)
    tokenData: TokenData = TokenService.tokenDataFromToken(token=token)
    # Assert
    assert tokenData.id() == "1234"
    assert tokenData.email() == "user_1@local.test"
