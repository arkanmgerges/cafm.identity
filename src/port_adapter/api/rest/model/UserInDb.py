"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from src.resource.api.model.User import User


class UserInDb(User):
    hashedPassword: str