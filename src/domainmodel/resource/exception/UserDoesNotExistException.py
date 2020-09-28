"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class UserDoesNotExistException(Exception):
    def __init__(self, username:str = ''):
        self.message = f'{username} does not exist'
        super().__init__(self.message)
