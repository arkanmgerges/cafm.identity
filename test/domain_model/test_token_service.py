"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

from src.domain_model.token.TokenData import TokenData
from src.domain_model.token.TokenService import TokenService


def test_generate_and_validate_token():
    # Arrange
    payload = {'id': '1234', 'name': 'john', 'role': ['super_admin']}
    # Act
    token = TokenService.generateToken(payload)
    tokenData: TokenData = TokenService.tokenDataFromToken(token=token)
    # Assert
    assert tokenData.id() == '1234'
    assert tokenData.name() == 'john'