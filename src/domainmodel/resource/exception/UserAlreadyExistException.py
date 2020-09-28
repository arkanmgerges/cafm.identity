"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class UserAlreadyExistException(Exception):
    def __init__(self, username: str = ''):
        self.message = f'{username} already exist'
        super().__init__(self.message)
