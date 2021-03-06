"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

import redis
from pyArango.connection import Connection
from pyArango.query import AQLQuery

from src.domain_model.authorization.AuthorizationRepository import (
    AuthorizationRepository,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class AuthorizationRepositoryImpl(AuthorizationRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
                username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
                password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
            )
            self._db = self._connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "")]
        except Exception as e:
            raise Exception(
                f"[{AuthorizationRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}"
            )

        try:
            self._cache = redis.Redis(
                host=os.getenv("CAFM_IDENTITY_REDIS_HOST", "localhost"),
                port=os.getenv("CAFM_IDENTITY_REDIS_PORT", 6379),
            )
            self._cacheSessionKeyPrefix = os.getenv(
                "CAFM_IDENTITY_REDIS_SESSION_KEY_PREFIX", "cafm.identity.session."
            )
        except Exception as e:
            raise Exception(
                f"[{AuthorizationRepositoryImpl.__init__.__qualname__}] Could not connect to the redis, message: {e}"
            )

    @debugLogger
    def rolesByUserId(self, id: str) -> List[str]:
        logger.debug(
            f"[{AuthorizationRepositoryImpl.rolesByUserId.__qualname__}] - with id: {id}"
        )
        aql = """
                WITH resource
                FOR u IN resource
                FILTER u.name == @name AND u.password == @password AND u.type == 'user'
                LET r1 = (FOR v,e IN 1..1 OUTBOUND u._id has FILTER e._to_type == "role" RETURN v)
                LET r2 = (
                            FOR ug IN resource
                            FILTER ug.type == 'user_group'
                            LET r3 = (FOR vUser,eUser IN 1..1 OUTBOUND ug._id has FILTER eUser._to_type == "user" AND vUser._id == u._id RETURN ug._id)
                            FOR vRole,eRole IN 1..1 OUTBOUND r3[0].ug._id has FILTER eRole._to_type == "role" RETURN vRole
                         )
                         LET r4 = union_distinct(r1, r2)
                         LET r5 = (FOR d5 IN r4 RETURN {"id": d5.id, "name": d5.name})
                        RETURN {'role': r5}
              """

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(
            aql, bindVars=bindVars, rawResults=True
        )
        result = queryResult.result
        if len(result) == 0:
            logger.info(
                f"[{AuthorizationRepositoryImpl.rolesByUserId.__qualname__}] - no result for user with id: {id}"
            )
            return []

        result = result[0]
        return result["role"]

    @debugLogger
    def tokenExists(self, token: str) -> bool:
        return self._cache.exists(f"{self._cacheSessionKeyPrefix}{token}") == 1
