"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""

class CafmClientConfig:
    def __init__(self, email=None, password=None, baseUrl=None, token=None, cache=None):
        self.email = email
        self.password = password
        self.baseUrl = baseUrl
        self.token = token
        self.cache = cache