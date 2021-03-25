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
from src.domain_model.resource.exception.UserGroupDoesNotExistException import UserGroupDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user_group.UserGroup import UserGroup
from src.domain_model.user_group.UserGroupRepository import UserGroupRepository
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class UserGroupRepositoryImpl(UserGroupRepository):
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
            logger.warn(f'[{UserGroupRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def save(self, obj: UserGroup, tokenData: TokenData = None):
        try:
            user = self.userGroupById(id=obj.id())
            if user != obj:
                self.updateUserGroup(obj=obj, tokenData=tokenData)
        except UserGroupDoesNotExistException as _e:
            self.createUserGroup(obj=obj, tokenData=tokenData)

    @debugLogger
    def createUserGroup(self, obj: UserGroup, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))

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
            'resource': {"id": obj.id(), "name": obj.name(), "type": obj.type()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)

    @debugLogger
    def updateUserGroup(self, obj: UserGroup, tokenData: TokenData) -> None:
        repoObj = self.userGroupById(obj.id())
        if repoObj != obj:
            aql = '''
                FOR d IN resource
                    FILTER d.id == @id AND d.type == 'user_group'
                    UPDATE d WITH {name: @name} IN resource
            '''

            bindVars = {"id": obj.id(),
                        "name": repoObj.name() if obj.name() is None else obj.name()}
            logger.debug(
                f'[{UserGroupRepositoryImpl.updateUserGroup.__qualname__}] - Update user group with id: {obj.id()}')
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

            # Check if it is updated
            repoObj = self.userGroupById(obj.id())
            if repoObj != obj:
                logger.warn(
                    f'[{UserGroupRepositoryImpl.updateUserGroup.__qualname__}] The object user group: {obj} could not be updated in the database')
                raise ObjectCouldNotBeUpdatedException(f'user group: {obj}')

    @debugLogger
    def deleteUserGroup(self, obj: UserGroup, tokenData: TokenData = None):
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
                'resource': {"id": obj.id(), "name": obj.name(), "type": obj.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.userGroupById(obj.id())
            logger.debug(
                f'[{UserGroupRepositoryImpl.deleteUserGroup.__qualname__}] Object could not be found exception for user group id: {obj.id()}')
            raise ObjectCouldNotBeDeletedException(f'user group id: {obj.id()}')

    @debugLogger
    def userGroupByName(self, name: str) -> UserGroup:
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'user_group'
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserGroupRepositoryImpl.userGroupByName.__qualname__}] {name}')
            raise UserGroupDoesNotExistException(name)

        return UserGroup.createFrom(id=result[0]['id'], name=result[0]['name'])

    @debugLogger
    def userGroupById(self, id: str) -> UserGroup:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user_group'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserGroupRepositoryImpl.userGroupById.__qualname__}] user group id: {id}')
            raise UserGroupDoesNotExistException(f'user group id: {id}')

        return UserGroup.createFrom(id=result[0]['id'], name=result[0]['name'])

    @debugLogger
    def userGroups(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData],
                   resultFrom: int = 0,
                   resultSize: int = 100,
                   order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.resourcesOfTypeByTokenData(PermissionContextConstant.USER_GROUP.value, tokenData,
                                                                roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]
        return {"items": [UserGroup.createFrom(id=x['id'], name=x['name']) for x in items],
                "itemCount": itemCount}
