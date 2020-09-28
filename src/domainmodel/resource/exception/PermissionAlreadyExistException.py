"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


class PermissionAlreadyExistException(Exception):
    def __init__(self, name: str = ''):
        self.message = f'{name} already exist'
        super().__init__(self.message)
