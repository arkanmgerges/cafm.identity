"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class RoleDoesNotExistException(Exception):
    def __init__(self, name:str = ''):
        self.message = f'{name} does not exist'
        super().__init__(self.message)
