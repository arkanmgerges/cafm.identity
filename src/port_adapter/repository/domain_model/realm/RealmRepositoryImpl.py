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
from src.domain_model.realm.Realm import Realm
from src.domain_model.realm.RealmRepository import RealmRepository
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.RealmDoesNotExistException import RealmDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class RealmRepositoryImpl(RealmRepository):
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
            logger.warn(f'[{RealmRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def createRealm(self, realm: Realm, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))
        # aql = '''
        # UPSERT {id: @id, type: 'realm'}
        #     INSERT {id: @id, name: @name, type: 'realm'}
        #     UPDATE {name: @name}
        #   IN resource
        # '''

        # bindVars = {"id": realm.id(), "name": realm.name()}
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
                    res = db.resource.insert({id: p['id'], name: p['name'], realm_type: p['realmType'], type: p['type']});
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
            'resource': {"id": realm.id(), "name": realm.name(), "type": realm.type(), "realmType": realm.realmType()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)

    @debugLogger
    def updateRealm(self, realm: Realm, tokenData: TokenData) -> None:
        oldObject = self.realmById(realm.id())
        if oldObject == realm:
            logger.debug(
                f'[{RealmRepositoryImpl.updateRealm.__qualname__}] Object identical exception for old realm: {oldObject}\nrealm: {realm}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'realm'
                UPDATE d WITH {name: @name, realm_type: @realmType} IN resource
        '''

        bindVars = {"id": realm.id(), "name": realm.name(), "realmType": realm.realmType()}
        logger.debug(f'[{RealmRepositoryImpl.updateRealm.__qualname__}] - Update realm with id: {realm.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        anObject = self.realmById(realm.id())
        if anObject != realm:
            logger.warn(
                f'[{RealmRepositoryImpl.updateRealm.__qualname__}] The object realm: {realm} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'realm: {realm}')

    @debugLogger
    def deleteRealm(self, realm: Realm, tokenData: TokenData):
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
                'resource': {"id": realm.id(), "name": realm.name(), "type": realm.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.realmById(realm.id())
            logger.debug(
                f'[{RealmRepositoryImpl.deleteRealm.__qualname__}] Object could not be found exception for realm id: {realm.id()}')
            raise ObjectCouldNotBeDeletedException(f'realm id: {realm.id()}')

    @debugLogger
    def realmByName(self, name: str) -> Realm:
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'realm'
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RealmRepositoryImpl.realmByName.__qualname__}] {name}')
            raise RealmDoesNotExistException(name)

        return Realm.createFrom(id=result[0]['id'], name=result[0]['name'])

    @debugLogger
    def realmById(self, id: str) -> Realm:
        aql = '''
            FOR d IN realm
                FILTER d.id == @id AND d.type == 'realm'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{RealmRepositoryImpl.realmById.__qualname__}] realm id: {id}')
            raise RealmDoesNotExistException(f'realm id: {id}')

        return Realm.createFrom(id=result[0]['id'], name=result[0]['name'])

    @debugLogger
    def realms(self, tokenData: TokenData, roleAccessPermissionData:List[RoleAccessPermissionData], resultFrom: int = 0, resultSize: int = 100,
                        order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.resourcesOfTypeByTokenData(PermissionContextConstant.REALM.value, tokenData, roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]
        return {"items": [Realm.createFrom(id=x['id'], name=x['name']) for x in items],
                "itemCount": itemCount}

