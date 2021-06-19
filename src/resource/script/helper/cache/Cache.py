"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

import redis


class Cache:
    CACHE_PREFIX = os.getenv('CACHE_PREFIX', 'cafm.identity.admin_script:')
    CACHE_TTL = os.getenv('CACHE_TTL', 43200)

    _instance = None

    def __init__(self):
        config = {
            "host": os.getenv("CAFM_IDENTITY_REDIS_HOST", "localhost"),
            "port": os.getenv("CAFM_IDENTITY_REDIS_PORT", 6379),
        }
        cache: redis.client.Redis = redis.Redis(**config)
        self._cache = cache

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Cache()
        return cls._instance

    def client(self) -> redis.Redis:
        return self._cache