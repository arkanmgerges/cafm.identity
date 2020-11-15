"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
from typing import List

from pyArango.connection import *
from pyArango.query import AQLQuery

import src.port_adapter.AppDi as AppDi
from src.domain_model.permission_context.PermissionContext import PermissionContextConstant
from src.domain_model.resource.exception.CodeExceptionConstant import CodeExceptionConstant
from src.domain_model.resource.exception.ObjectCouldNotBeDeletedException import ObjectCouldNotBeDeletedException
from src.domain_model.resource.exception.ObjectCouldNotBeUpdatedException import ObjectCouldNotBeUpdatedException
from src.domain_model.resource.exception.ObjectIdenticalException import ObjectIdenticalException
from src.domain_model.resource.exception.UserDoesNotExistException import UserDoesNotExistException
from src.domain_model.token.TokenData import TokenData
from src.domain_model.user.User import User
from src.domain_model.user.UserRepository import UserRepository
from src.port_adapter.repository.domain_model.helper.HelperRepository import HelperRepository
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
        except Exception as e:
            logger.warn(f'[{UserRepositoryImpl.__init__.__qualname__}] Could not connect to the db, message: {e}')
            raise Exception(f'Could not connect to the db, message: {e}')

    def createUser(self, user: User, tokenData: TokenData):
        userDocId = self._helperRepo.userDocumentId(id=tokenData.id())
        rolesDocIds = []
        roles = tokenData.roles()
        for role in roles:
            rolesDocIds.append(self._helperRepo.roleDocumentId(id=role['id']))
        # aql = '''
        # UPSERT {id: @id, type: 'user'}
        #     INSERT {id: @id, name: @name, type: 'user'}
        #     UPDATE {name: @name}
        #   IN resource
        # '''

        # bindVars = {"id": user.id(), "name": user.name()}
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
                    for (let i = 0; i < params['usersDocIds'].length; i++) {
                        let currentDocId = params['usersDocIds'][i];
                        let p = {'fromId': fromDocId, 'toId': currentDocId, 
                            'fromType': params['resource']['type'], 'toType': params['toTypeUser']};
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
            'resource': {"id": user.id(), "name": user.name(), "type": user.type()},
            'user': {"toId": userDocId, "toType": PermissionContextConstant.USER.value},
            'rolesDocIds': rolesDocIds,
            'toTypeRole': PermissionContextConstant.ROLE.value,
            'OBJECT_ALREADY_EXIST_CODE': CodeExceptionConstant.OBJECT_ALREADY_EXIST.value
        }
        self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)

    def updateUser(self, user: User, tokenData: TokenData) -> None:
        oldObject = self.userById(user.id())
        if oldObject == user:
            logger.debug(
                f'[{UserRepositoryImpl.updateUser.__qualname__}] Object identical exception for old user: {oldObject}\nuser: {user}')
            raise ObjectIdenticalException()

        aql = '''
            FOR d IN resource
                FILTER d.id == @id AND d.type == 'user'
                UPDATE d WITH {name: @name} IN resource
        '''

        bindVars = {"id": user.id(), "name": user.name()}
        logger.debug(f'[{UserRepositoryImpl.updateUser.__qualname__}] - Update user with id: {user.id()}')
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        _ = queryResult.result

        # Check if it is updated
        anObject = self.userById(user.id())
        if anObject != user:
            logger.warn(
                f'[{UserRepositoryImpl.updateUser.__qualname__}] The object user: {user} could not be updated in the database')
            raise ObjectCouldNotBeUpdatedException(f'user: {user}')

    def deleteUser(self, user: User, tokenData: TokenData):
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
                'resource': {"id": user.id(), "name": user.name(), "type": user.type()},
                'OBJECT_DOES_NOT_EXIST_CODE': CodeExceptionConstant.OBJECT_DOES_NOT_EXIST.value
            }
            self._db.transaction(collections={'write': ['resource', 'owned_by']}, action=actionFunction, params=params)
        except Exception as e:
            print(e)
            self.userById(user.id())
            logger.debug(
                f'[{UserRepositoryImpl.deleteUser.__qualname__}] Object could not be found exception for user id: {user.id()}')
            raise ObjectCouldNotBeDeletedException(f'user id: {user.id()}')

    def userByName(self, name: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByName.__qualname__}] - with name = {name}')
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.type == 'user'
                RETURN d
        '''

        bindVars = {"name": name}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userByName.__qualname__}] {name}')
            raise UserDoesNotExistException(name)

        return User.createFrom(id=result[0]['id'], name=result[0]['name'], password=result[0]['password'])

    def userByNameAndPassword(self, name: str, password: str) -> User:
        logger.debug(f'[{UserRepositoryImpl.userByNameAndPassword.__qualname__}] - with name = {name}')
        aql = '''
            FOR d IN resource
                FILTER d.name == @name AND d.password == @password AND d.type == 'user'
                RETURN d
        '''

        bindVars = {"name": name, "password": password}
        queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
        result = queryResult.result
        if len(result) == 0:
            logger.debug(f'[{UserRepositoryImpl.userByNameAndPassword.__qualname__}] name: {name}')
            raise UserDoesNotExistException(name)

        return User.createFrom(id=result[0]['id'], name=result[0]['name'], password=result[0]['password'])

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

        return User.createFrom(id=result[0]['id'], name=result[0]['name'])

    def usersByOwnedRoles(self, ownedRoles: List[str], resultFrom: int = 0, resultSize: int = 100,
                          order: List[dict] = None) -> dict:
        sortData = ''
        if order is not None:
            for item in order:
                sortData = f'{sortData}, d.{item["orderBy"]} {item["direction"]}'
            sortData = sortData[2:]
        if 'super_admin' in ownedRoles:
            aql = '''
                LET ds = (FOR d IN resource FILTER d.type == 'user' #sortData RETURN d)
                RETURN {items: SLICE(ds, @resultFrom, @resultSize), itemCount: LENGTH(ds)}
            '''
            if sortData != '':
                aql = aql.replace('#sortData', f'SORT {sortData}')
            else:
                aql = aql.replace('#sortData', '')

            bindVars = {"resultFrom": resultFrom, "resultSize": resultSize}
            queryResult: AQLQuery = self._db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
            result = queryResult.result
            if len(result) == 0:
                return {"items": [], "itemCount": 0}
            return {"items": [User.createFrom(id=x['id'], name=x['name']) for x in result[0]['items']],
                    "itemCount": result[0]["itemCount"]}
