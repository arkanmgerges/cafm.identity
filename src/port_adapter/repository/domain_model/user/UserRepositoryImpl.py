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
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
from src.resource.logging.decorator import debugLogger
from src.resource.logging.logger import logger


class UserRepositoryImpl(UserRepository):
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
            logger.warn(f'[{UserRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    @debugLogger
    def createUser(self, obj: User, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))
        # aql = '''
        # UPSERT {id: @id, type: 'user'}
        #     INSERT {id: @id, email: @email, type: 'user'}
        #     UPDATE {email: @email}
        #   IN resource
        # '''

        # bindVars = {"id": user.id(), "email": user.email()}
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
                    res = db.resource.insert({id: p['id'], email: p['email'], password: p['password'], 
                                              type: p['type']});
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
            'resource': {"id": obj.id(), "email": obj.email(), "password": obj.password(), "type": obj.type()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params,
                             waitForSync=True)

    @debugLogger
    def updateUser(self, obj: User, tokenData: TokenData) -> None:
        repoObj = self.userById(obj.id())
        if repoObj == obj:
            logger.debug(
                f'[{UserRepositoryImpl.updateUser.__qualname__}] Object identical exception for old user: {repoObj}\nuser: {obj}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                UPDATE d WITH {email: @email} IN resource
        '''

        bindVars = {"id": obj.id(), "email": obj.email()}
        logger.debug(f'[{UserRepositoryImpl.updateUser.__qualname__}] - Update user with id: {obj.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        repoObj = self.userById(obj.id())
        if repoObj != obj:
            logger.warn(
                f'[{UserRepositoryImpl.updateUser.__qualname__}] The object user: {obj} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'user: {obj.toMap()}')

    @debugLogger
    def deleteUser(self, obj: User, tokenData: TokenData):
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
                'resource': {"id": obj.id(), "email": obj.email(), "type": obj.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.userById(obj.id())
            logger.debug(
                f'[{UserRepositoryImpl.deleteUser.__qualname__}] Object could not be found exception for user id: {obj.id()}')
            raise ObjectCouldNotBeDeletedException(f'user id: {obj.id()}')

    @debugLogger
    def deleteUserOneTimePassword(self, obj: User, tokenData: TokenData):
        oldObject = self.userById(obj.id())
        if oldObject.isPasswordOneTimePassword():
            aql = '''
                        FOR d IN resource
                            FILTER d.id == @id AND d.type == 'user'
                            UPDATE d WITH {password: ""} IN resource
                    '''

            logger.debug(f'[{UserRepositoryImpl.deleteUserOneTimePassword.__qualname__}] - Delete user password with user id: {obj.id()}')
            bindVars = {"id": obj.id()}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            _ = queryResult.result

    @debugLogger
    def setUserPassword(self, obj: User, tokenData: TokenData):
        aql = '''
                    FOR d IN resource
                        FILTER d.id == @id AND d.type == 'user'
                        UPDATE d WITH {password: @password} IN resource
                '''

        logger.debug(f'[{UserRepositoryImpl.setUserPassword.__qualname__}] - Set user password with user id: {obj.id()}')
        bindVars = {"id": obj.id(), "password": obj.password()}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

    @debugLogger
    def userByEmail(self, email: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByEmail.__qualname__}] - with email = {email}')
        aql = '''
            FOR d IN resource
                FILTER d.email == @email AND d.type == 'user'
                RETURN d
        '''

        bindVars = {"email": email}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userByEmail.__qualname__}] {email}')
            raise UserDoesNotExistException(email)

        return User.createFrom(**self._constructUserDictFromResult(result[0]))

    @debugLogger
    def userByEmailAndPassword(self, email: str, password: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByEmailAndPassword.__qualname__}] - with email = {email}')
        aql = '''
            FOR d IN resource
                FILTER d.email == @email AND d.password == @password AND d.type == 'user'
                RETURN d
        '''

        bindVars = {"email": email, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userByEmailAndPassword.__qualname__}] email: {email}')
            raise UserDoesNotExistException(email)

        return User.createFrom(**self._constructUserDictFromResult(result[0]))

    @debugLogger
    def userById(self, id: str) -> User:
        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                RETURN d
        '''

        bindVars = {"id": id}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userById.__qualname__}] user id: {id}')
            raise UserDoesNotExistException(f'user id: {id}')

        return User.createFrom(**self._constructUserDictFromResult(result[0]))

    @debugLogger
    def _constructUserDictFromResult(self, result) -> dict:
        return {
            'id': result['id'] if 'id' in result and result['id'] is not None else None,
            'email': result['email'] if 'email' in result else '',
            'password': result['password'] if 'password' in result else ''
        }

    @debugLogger
    def users(self, tokenData: TokenData, roleAccessPermissionData: List[RoleAccessPermissionData], resultFrom: int = 0,
              resultSize: int = 100,
              order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]

        result = self._policyService.resourcesOfTypeByTokenData(PermissionContextConstant.USER.value, tokenData,
                                                                roleAccessPermissionData, sortData)

        if result is None or len(result['items']) == 0:
            return {"items": [], "itemCount": 0}
        items = result['items']
        itemCount = len(items)
        items = items[resultFrom:resultFrom + resultSize]
        return {"items": [User.createFrom(id=x['id'], email=x['email'],
                                          password=x['password'] if 'password' in x else '',) for x in items],
                "itemCount": itemCount}
