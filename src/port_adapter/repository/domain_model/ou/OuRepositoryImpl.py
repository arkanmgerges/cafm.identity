"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.ou.Ou import Ou
from src.domain_model.ou.OuRepository import OuRepository
from src.domain_model.permission_context.PermissionContext import (
    PermissionContextConstant,
)
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.CodeExceptionConstant import (
    CodeExceptionConstant,
)
from src.domain_model.resource.exception.InvalidValueException import InvalidValueException
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import (
    ObjectCouldNotBeDeletedException,
)
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import (
    ObjectCouldNotBeUpdatedException,
)
from src.domain_model.resource.exception.OuDoesNotExistException import (
    OuDoesNotExistException,
)
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import (
    HelperRepository,
)
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class OuRepositoryImpl(OuRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv("CAFM_IDENTITY_ARANGODB_URL", ""),
                username=os.getenv("CAFM_IDENTITY_ARANGODB_USERNAME", ""),
                password=os.getenv("CAFM_IDENTITY_ARANGODB_PASSWORD", ""),
            )
            self._db = self._connection[os.getenv("CAFM_IDENTITY_ARANGODB_DB_NAME", "")]
            self._helperRepo: HelperRepository = AppDi.instance.get(HelperRepository)
            self._policyService: PolicyControllerService = AppDi.instance.get(PolicyControllerService)
        except Exception as e:
            logger.warn(f"[{OuRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}")
            raise Exception(f"Could not connect to the db, message: {e}")

    @debugLogger
    def save(self, obj: Ou, tokenData: TokenData = None):
        try:
            user = self.ouById(id=obj.id())
            if user != obj:
                self.updateOu(obj=obj, tokenData=tokenData)
        except OuDoesNotExistException as _e:
            self.createOu(obj=obj, tokenData=tokenData)

    @debugLogger
    def createOu(self, obj: Ou, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role["id"]))
        # aql = '''
        # UPSERT {id: @id, type: 'ou'}
        #     INSERT {id: @id, name: @name, type: 'ou'}
        #     UPDATE {name: @name}
        #   IN resource
        # '''

        # bindVars = {"id": ou.id(), "name": ou.name()}
        # queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        actionFunction = """
            function (params) {                                            
                queryLink = `UPSERT {_from: @fromId, _to: @toId}
                      INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                      UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                     IN owned_by`;
                
                let db = require('@arangodb').db;
                let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                if (res.length == 0) {
                    p = params['resource']
                    res = db.resource.insert({_key: p['id'], id: p['id'], name: p['name'], type: p['type']});
                    fromDocId = res['_id'];
                    p = params['user']; p['fromId'] = fromDocId; p['fromType'] = params['resource']['type'];
                    db._query(queryLink, p).execute();
                    for (let i = 0; i < params['rolesDocIds'].length; i++) {
                        let currentDocId = params['rolesDocIds'][i];
                        let p = {'fromId': fromDocId, 'toId': currentDocId, 
                            'fromType': params['resource']['type'], 'toType': params['toTypeRole']};
                        db._query(queryLink, p).execute();    
                    }
                } else {
                    let err = new Error(`Could not create resource, ${params['resource']['id']} is already exist`);
                    err.errorNum = params['OBJECT_ALREADY_EXIST_CODE'];
                    throw err;
                }
            }
        """
        params = {
            "resource": {"id": obj.id(), "name": obj.name(), "type": obj.type()},
            "user": {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            "rolesDocIds": rolesDocIds,
            "toTypeRole": PermissionContextConstant.ROLE.value,
            "OBJECT_ALREADY_EXIST_CODE": CodeExceptionConstant.OBJECT_ALREADY_EXIST.value,
        }
        try:
            self._db.transaction(
                collections={"write": ["resource", "owned_by"]},
                action=actionFunction,
                params=params,
            )
        except Exception as e:
            raise InvalidValueException(message=e.message)

    @debugLogger
    def deleteOu(self, obj: Ou, tokenData: TokenData = None):
        try:
            actionFunction = """
                function (params) {                                            

                    let db = require('@arangodb').db;
                    let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                    if (res.length != 0) {
                        let doc = res[0];
                        let edges = db.owned_by.outEdges(doc._id);   
                        for (let i = 0; i < edges.length; i++) {
                            db.owned_by.remove(edges[i]);
                        }
                        edges = db.has.edges(doc._id);   
                        for (let i = 0; i < edges.length; i++) {
                            db.has.remove(edges[i]);
                        }
                        edges = db.access.edges(doc._id);   
                        for (let i = 0; i < edges.length; i++) {
                            db.access.remove(edges[i]);
                        }
                        db.resource.remove(doc);
                    } else {
                        let err = new Error(`Could not delete resource, ${params['resource']['id']}, it does not exist`);
                        err.errorNum = params['OBJECT_DOES_NOT_EXIST_CODE'];
                        throw err;
                    }
                }
            """
            params = {
                "resource": {"id": obj.id(), "name": obj.name(), "type": obj.type()},
                "OBJECT_DOES_NOT_EXIST_CODE": CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value,
            }

            from src.domain_model.policy.PolicyRepository import PolicyRepository

            policyRepo: PolicyRepository = AppDi.instance.get(PolicyRepository)
            policyRepo.deleteRolesTreesCache()
            self._db.transaction(
                collections={"write": ["resource", "owned_by", "has", "access"]},
                action=actionFunction,
                params=params,
            )
            from src.domain_model.policy.PolicyRepository import PolicyRepository
            policyRepo: PolicyRepository = AppDi.instance.get(PolicyRepository)
            policyRepo.deleteRolesTreesCache()
        except Exception as e:
            self.ouById(obj.id())
            logger.debug(
                f"[{OuRepositoryImpl.deleteOu.__qualname__}] Object could not be found exception for ou id: {obj.id()}, exception: {e}"
            )
            raise ObjectCouldNotBeDeletedException(f"ou id: {obj.id()}")

    @debugLogger
    def updateOu(self, obj: Ou, tokenData: TokenData) -> None:
        repoObj = self.ouById(obj.id())
        if repoObj != obj:
            aql = """
                FOR d IN resource
                    FILTER d.id == @id AND d.type == 'ou'
                    UPDATE d WITH {name: @name} IN resource
            """

            bindVars = {
                "id": obj.id(),
                "name": repoObj.name() if obj.name() is None else obj.name(),
            }
            logger.debug(f"[{OuRepositoryImpl.updateOu.__qualname__}] - Update ou with id: {obj.id()}")
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

            # Check if it is updated
            repoObj = self.ouById(obj.id())
            if repoObj != obj:
                logger.warn(
                    f"[{OuRepositoryImpl.updateOu.__qualname__}] The object ou: {obj} could not be updated in the database"
                )
                raise ObjectCouldNotBeUpdatedException(f"ou: {obj}")

    @debugLogger
    def ouByName(self, name: str) -> Ou:
        aql = """
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'ou' 
                RETURN d
        """

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f"[{OuRepositoryImpl.ouByName.__qualname__}] {name}")
            raise OuDoesNotExistException(name)

        return Ou.createFrom(id=result[0]["id"], name=result[0]["name"])

    @debugLogger
    def ouById(self, id: str) -> Ou:
        aql = """
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'ou'
                RETURN d
        """

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f"[{OuRepositoryImpl.ouById.__qualname__}] ou id: {id}")
            raise OuDoesNotExistException(f"ou id: {id}")

        return Ou.createFrom(id=result[0]["id"], name=result[0]["name"])

    @debugLogger
    def ous(
        self,
        tokenData: TokenData,
        roleAccessPermissionData: List[RoleAccessPermissionData],
        resultFrom: int = 0,
        resultSize: int = 100,
        order: List[dict] = None,
    ) -> dict:
        sortData = ""
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.resourcesOfTypeByTokenData(
            PermissionContextConstant.OU.value,
            tokenData,
            roleAccessPermissionData,
            sortData,
        )

        if result is None or len(result["items"]) == 0:
            return {"items": [], "totalItemCount": 0}
        items = result["items"]
        totalItemCount = len(items)
        items = items[resultFrom : resultFrom + resultSize]
        return {
            "items": [Ou.createFrom(id=x["id"], name=x["name"]) for x in items],
            "totalItemCount": totalItemCount,
        }
