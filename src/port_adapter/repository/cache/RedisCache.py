"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

import redis
from redis.client import Redis


class RedisCache:
    def __init__(self):
        try:
            self._cache: Redis = redis.Redis(
                host=os.getenv("CAFM_IDENTITY_REDIS_HOST", "localhost"),
                port=os.getenv("CAFM_IDENTITY_REDIS_PORT", 6379),
            )
            self._cacheResponseKeyPrefix = os.getenv(
                "CAFM_API_REDIS_RSP_KEY_PREFIX", "cafm.api.rsp"
            )
            self._cacheSessionPrefix = os.getenv(
                "CAFM_IDENTITY_REDIS_SESSION_KEY_PREFIX", "cafm.identity.session."
            )
            self._refreshTokenTtl = int(
                os.getenv("CAFM_IDENTITY_USER_AUTH_TTL_IN_SECONDS", 300)
            )
        except Exception as e:
            raise Exception(
                f"[{RedisCache.__init__.__qualname__}] Could not connect to the redis, message: {e}"
            )

    def client(self) -> Redis:
        return self._cache

    def cacheResponseKeyPrefix(self):
        return self._cacheResponseKeyPrefix

    def cacheSessionKeyPrefix(self):
        return self._cacheSessionPrefix

    def refreshTokenTtl(self):
        return self._refreshTokenTtl
