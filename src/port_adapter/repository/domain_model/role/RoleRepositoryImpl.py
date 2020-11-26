"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.policy.PolicyControllerService import PolicyControllerService
from src.domain_model.policy.RoleAccessPermissionData import RoleAccessPermissionData
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.RoleDoesNotExistException import RoleDoesNotExistException
from src.domain_model.role.Role import Role
from src.domain_model.role.RoleRepository import RoleRepository
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.logger import logger


class RoleRepositoryImpl(RoleRepository):
    def __init__(self):
        try:
            self._connection = Connection(
                arangoURL=os.getenv('CAFM_IDENTITY_ARANGODB_URL', ''),
                username=os.getenv('CAFM_IDENTITY_ARANGODB_USERNAME', ''),
                password=os.getenv('CAFM_IDENTITY_ARANGODB_PASSWORD', '')
            )
            self._db = self._connection[os.getenv('CAFM_IDENTITY_ARANGODB_DB_NAME', '')]
            self._helperRepo: HelperRepository = AppDi.instance.get(HelperRepository)
            self._policyService: PolicyControllerService = AppDi.instance.get(PolicyControllerService)
        except Exception as e:
            logger.warn(f'[{RoleRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def createRole(self, role: Role, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))
        # aql = '''
        # UPSERT {id: @id, type: 'role'}
        #     INSERT {id: @id, name: @name, type: 'role'}
        #     UPDATE {name: @name}
        #   IN resource
        # '''

        # bindVars = {"id": role.id(), "name": role.name()}
        # queryResult = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)

        actionFunction = '''
            function (params) {                                            
                queryLink = `UPSERT {_from: @fromId, _to: @toId}
                      INSERT {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                      UPDATE {_from: @fromId, _to: @toId, _from_type: @fromType, _to_type: @toType}
                     IN owned_by`;

                let db = require('@arangodb').db;
                let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                if (res.length == 0) {
                    p = params['resource']
                    res = db.resource.insert({id: p['id'], name: p['name'], type: p['type']});
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
        '''
        params = {
            'resource': {"id": role.id(), "name": role.name(), "type": role.type()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)

    def updateRole(self, role: Role, tokenData: TokenData) -> None:
        oldObject = self.roleById(role.id())
        if oldObject == role:
            logger.debug(
                f'[{RoleRepositoryImpl.updateRole.__qualname__}] Object identical exception for old role: {oldObject}\nrole: {role}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'role'
                UPDATE d WITH {name: @name} IN resource
        '''

        bindVars = {"id": role.id(), "name": role.name()}
        logger.debug(f'[{RoleRepositoryImpl.updateRole.__qualname__}] - Update role with id: {role.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        anObject = self.roleById(role.id())
        if anObject != role:
            logger.warn(
                f'[{RoleRepositoryImpl.updateRole.__qualname__}] The object role: {role} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'role: {role}')

    def deleteRole(self, role: Role, tokenData: TokenData):
        try:
            actionFunction = '''
                function (params) {                                            

                    let db = require('@arangodb').db;
                    let res = db.resource.byExample({id: params['resource']['id'], type: params['resource']['type']}).toArray();
                    if (res.length != 0) {
                        let doc = res[0];
                        let edges = db.owned_by.outEdges(doc._id);   
                        for (let i = 0; i < edges.length; i++) {
                            db.owned_by.remove(edges[i]);
                        }
                        db.resource.remove(doc);
                    } else {
                        let err = new Error(`Could not delete resource, ${params['resource']['id']}, it does not exist`);
                        err.errorNum = params['OBJECT_DOES_NOT_EXIST_CODE'];
                        throw err;
                    }
                }
            '''
            params = {
                'resource': {"id": role.id(), "name": role.name(), "type": role.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.roleById(role.id())
            logger.debug(
                f'[{RoleRepositoryImpl.deleteRole.__qualname__}] Object could not be found exception for role id: {role.id()}')
            raise ObjectCouldNotBeDeletedException(f'role id: {role.id()}')

    def roleByName(self, name: str) -> Role:
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'role'
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RoleRepositoryImpl.roleByName.__qualname__}] {name}')
            raise RoleDoesNotExistException(name)

        return Role.createFrom(id=result[0]['id'], name=result[0]['name'])

    def roleById(self, id: str) -> Role:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'role'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RoleRepositoryImpl.roleById.__qualname__}] role id: {id}')
            raise RoleDoesNotExistException(f'role id: {id}')

        return Role.createFrom(id=result[0]['id'], name=result[0]['name'])

    def roles(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData], resultFrom: int = 0,
              resultSize: int = 100,
              order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.resourcesOfTypeByTokenData(PermissionContextConstant.ROLE.value, tokenData,
                                                                roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultSize]
        return {"items": [Role.createFrom(id=x['id'], name=x['name']) for x in items],
                "itemCount": itemCount}

    def rolesTrees(self, tokenData: TokenData, roleAccessPermissionDataList: List[RoleAccessPermissionData]) -> List[
        RoleAccessPermissionData]:
        logger.debug(
            f'[{RoleRepositoryImpl.rolesTrees.__qualname__}] Received tokenData: {tokenData}, roleAccessPermissionDataList: {roleAccessPermissionDataList}')
        result = self._policyService.rolesTrees(tokenData, roleAccessPermissionDataList)

        if result is None or len(result) == 0:
            return []
        return result

    def roleTree(self, tokenData: TokenData, roleId: str,
                 roleAccessPermissionData: List[RoleAccessPermissionData]) -> RoleAccessPermissionData:
        logger.debug(
            f'[{RoleRepositoryImpl.roleTree.__qualname__}] Received tokenData: {tokenData}, roleAccessPermissionData: {roleAccessPermissionData}')
        result = self._policyService.roleTree(tokenData, roleId, roleAccessPermissionData)

        return result
